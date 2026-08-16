import json
import os
import sys
import uuid
import re
import secrets
import hashlib
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_db_connection, query_as_dicts

PORT = int(os.getenv("PORT", 5000))
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

PASSCODE_CHARS = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

def hash_password(password, salt=None):
    """Securely hash a password using PBKDF2 with SHA-256 and a random salt."""
    if not salt:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return f"{salt}${pwd_hash}"

def verify_password(password, stored_hash):
    """Verify a plain password against the stored salt$hash string."""
    try:
        if not stored_hash or '$' not in stored_hash:
            return False
        salt, pwd_hash = stored_hash.split('$', 1)
        test_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        return secrets.compare_digest(pwd_hash, test_hash)
    except Exception:
        return False

def generate_ticket_passcode(length=6):
    """Generates a secure, unambiguous 6-character uppercase alphanumeric passcode."""
    return ''.join(secrets.choice(PASSCODE_CHARS) for _ in range(length))

def parse_ticket_code(raw_code):
    """
    Parses scanned barcode strings or manually typed ticket IDs into structured components.
    Supported patterns:
    - "A - 113005", "A-113005", "C-113005" (Zone + Prefix + ZoneDigit + TicketNum)
    - "113005" (Pure numeric: Prefix 11, Zone 3=C, Ticket 005=5)
    - "*A-111001*" or "*112004*" (Barcode reader wrapping with asterisks)
    - "A - 1" (Legacy zone + number)
    """
    if not raw_code:
        return None
    
    clean = str(raw_code).strip().strip('*').strip()
    
    # Pattern 1: Zone Letter + Dash/Space + (Prefix)(ZoneDigit)(TicketNum)
    m = re.match(r'^([A-Za-z])\s*[-_]?\s*(\d{2,})(\d)(\d{3,})$', clean)
    if m:
        zone_letter = m.group(1).upper()
        show_prefix = m.group(2)
        zone_digit = int(m.group(3))
        ticket_num = int(m.group(4))
        return {
            "show_prefix": show_prefix,
            "zone_name": zone_letter,
            "ticket_number": ticket_num,
            "raw": clean
        }

    # Pattern 2: Pure Numeric e.g., "113005" -> Prefix 11, ZoneDigit 3 (C), Ticket 005 (5)
    m = re.match(r'^(\d{2,})(\d)(\d{3,})$', clean)
    if m:
        show_prefix = m.group(1)
        zone_digit = int(m.group(2))
        ticket_num = int(m.group(3))
        zone_letter = chr(ord('A') + zone_digit - 1) if 1 <= zone_digit <= 26 else 'A'
        return {
            "show_prefix": show_prefix,
            "zone_name": zone_letter,
            "ticket_number": ticket_num,
            "raw": clean
        }
    
    # Pattern 3: Zone Letter + Number (e.g. "A - 1001" or legacy "A - 1")
    m = re.match(r'^([A-Za-z])\s*[-_]?\s*(\d+)$', clean)
    if m:
        zone_letter = m.group(1).upper()
        num_part = m.group(2)
        if len(num_part) >= 5:
            show_prefix = num_part[:2]
            ticket_num = int(num_part[2:])
            return {
                "show_prefix": show_prefix,
                "zone_name": zone_letter,
                "ticket_number": ticket_num,
                "raw": clean
            }
        else:
            return {
                "show_prefix": None,
                "zone_name": zone_letter,
                "ticket_number": int(num_part),
                "raw": clean
            }
            
    return None

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

class TheatreHTTPHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Override to keep console cleaner, or redirect logs
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))

    def end_headers(self):
        # Add CORS headers for developer convenience
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        # API routing
        if self.path == '/api/shows':
            self.handle_get_shows()
        elif self.path == '/api/logs':
            self.handle_get_logs()
        elif self.path == '/api/gate/stats':
            self.handle_get_gate_stats()
        elif self.path == '/api/users':
            self.handle_get_users()
        else:
            # Static files serving
            self.handle_static_files()

    def do_POST(self):
        # Parse JSON content length
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            body = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON format"}, 400)
            return

        if self.path == '/api/auth/login':
            self.handle_auth_login(body)
        elif self.path == '/api/users':
            self.handle_create_user(body)
        elif self.path == '/api/users/delete':
            self.handle_delete_user(body)
        elif self.path == '/api/users/change-password':
            self.handle_change_password(body)
        elif self.path == '/api/shows':
            self.handle_create_show(body)
        elif self.path == '/api/shows/update':
            self.handle_update_show(body)
        elif self.path == '/api/shows/delete':
            self.handle_delete_show(body)
        elif self.path == '/api/shows/toggle-gate':
            self.handle_toggle_gate_show(body)
        elif self.path == '/api/shows/batch-gate':
            self.handle_batch_gate_shows(body)
        elif self.path == '/api/devices/register':
            self.handle_register_device(body)
        elif self.path == '/api/tickets/print':
            self.handle_print_ticket(body)
        elif self.path == '/api/tickets/verify':
            self.handle_verify_ticket(body)
        elif self.path == '/api/zones/update':
            self.handle_update_zone(body)
        elif self.path == '/api/zones/refill-all':
            self.handle_refill_all_seats(body)
        elif self.path == '/api/user/ticket-login':
            self.handle_user_ticket_login(body)
        elif self.path == '/api/logs/clear':
            self.handle_clear_logs(body)
        else:
            self.send_json({"error": "Not Found"}, 404)

    def send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        response_bytes = json.dumps(data, cls=CustomJSONEncoder).encode('utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    # Handlers
    def handle_static_files(self):
        # Normalize and resolve path
        raw_clean_path = self.path.split('?')[0]
        clean_path = urllib.parse.unquote(raw_clean_path)
        if clean_path == '/' or clean_path == '':
            clean_path = '/my-ticket.html'
            
        file_path = os.path.abspath(os.path.join(STATIC_DIR, clean_path.lstrip('/\\')))
        
        # Security: Prevent Directory Traversal
        if not file_path.startswith(STATIC_DIR) or not os.path.exists(file_path) or os.path.isdir(file_path):
            # Fallback to my-ticket.html for Single-Page-App routing
            file_path = os.path.join(STATIC_DIR, 'my-ticket.html')
            if not os.path.exists(file_path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")
                return

        # Determine MIME Content-Type
        content_type = "text/plain"
        if file_path.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif file_path.endswith(".css"):
            content_type = "text/css"
        elif file_path.endswith(".js"):
            content_type = "application/javascript"
        elif file_path.endswith(".png"):
            content_type = "image/png"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            content_type = "image/jpeg"
        elif file_path.endswith(".ico"):
            content_type = "image/x-icon"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            # Disable browser caching for instant code delivery
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"500 Internal Server Error: {str(e)}".encode('utf-8'))

    def handle_get_shows(self):
        conn = None
        try:
            conn = get_db_connection()
            shows = query_as_dicts(conn, "SELECT id, name, prefix, date, time, end_time, COALESCE(is_gate_active, TRUE) as is_gate_active FROM shows ORDER BY date ASC, time ASC, id ASC")
            for show in shows:
                zones = query_as_dicts(
                    conn,
                    "SELECT id, zone_name, total_capacity, available_seats FROM zones WHERE show_id = %s ORDER BY zone_name",
                    [show["id"]]
                )
                show["zones"] = zones
            self.send_json(shows)
        except Exception as e:
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_create_show(self, body):
        name = body.get("name")
        prefix = body.get("prefix", "").strip()
        date_val = body.get("date")
        time_val = body.get("time") or body.get("startTime")
        end_time_val = body.get("endTime") or body.get("end_time") or ""
        is_gate_active = body.get("is_gate_active", True)
        zones = body.get("zones", [])

        if not name or not date_val or not time_val or not zones:
            self.send_json({"error": "Missing required fields"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO shows (name, prefix, date, time, end_time, is_gate_active) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
                [name, prefix, date_val, time_val, end_time_val, bool(is_gate_active)]
            )
            show_id = cursor.fetchone()[0]
            
            for zone in zones:
                z_name = zone.get("zone_name")
                cap = int(zone.get("capacity", 0))
                cursor.execute(
                    "INSERT INTO zones (show_id, zone_name, total_capacity, available_seats) VALUES (%s, %s, %s, %s);",
                    [show_id, z_name, cap, cap]
                )
            
            conn.commit()
            self.send_json({"success": True, "showId": show_id}, 201)
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database transaction failed: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_update_show(self, body):
        show_id = body.get("id") or body.get("showId")
        name = body.get("name")
        prefix = body.get("prefix", "").strip()
        date_val = body.get("date")
        time_val = body.get("time") or body.get("startTime")
        end_time_val = body.get("endTime") or body.get("end_time") or ""
        is_gate_active = body.get("is_gate_active")

        if not show_id or not name or not date_val or not time_val:
            self.send_json({"error": "Missing required fields"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if is_gate_active is not None:
                cursor.execute(
                    """
                    UPDATE shows 
                    SET name = %s, prefix = %s, date = %s, time = %s, end_time = %s, is_gate_active = %s
                    WHERE id = %s;
                    """,
                    [name, prefix, date_val, time_val, end_time_val, bool(is_gate_active), int(show_id)]
                )
            else:
                cursor.execute(
                    """
                    UPDATE shows 
                    SET name = %s, prefix = %s, date = %s, time = %s, end_time = %s 
                    WHERE id = %s;
                    """,
                    [name, prefix, date_val, time_val, end_time_val, int(show_id)]
                )
            conn.commit()
            self.send_json({"success": True, "message": "Show updated successfully"})
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_toggle_gate_show(self, body):
        show_id = body.get("showId") or body.get("id")
        is_active = body.get("is_gate_active")
        if show_id is None or is_active is None:
            self.send_json({"error": "Missing showId or is_gate_active"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE shows SET is_gate_active = %s WHERE id = %s;",
                [bool(is_active), int(show_id)]
            )
            conn.commit()
            self.send_json({"success": True, "showId": int(show_id), "is_gate_active": bool(is_active)})
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_batch_gate_shows(self, body):
        active_ids = body.get("activeShowIds", [])
        set_all = body.get("setAll")
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if set_all is True:
                cursor.execute("UPDATE shows SET is_gate_active = TRUE;")
            elif set_all is False:
                cursor.execute("UPDATE shows SET is_gate_active = FALSE;")
            else:
                cursor.execute("UPDATE shows SET is_gate_active = FALSE;")
                if active_ids:
                    for s_id in active_ids:
                        cursor.execute("UPDATE shows SET is_gate_active = TRUE WHERE id = %s;", [int(s_id)])
            conn.commit()
            self.send_json({"success": True})
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_delete_show(self, body):
        show_id = body.get("id") or body.get("showId")
        if not show_id:
            self.send_json({"error": "Missing show ID"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ticket_logs WHERE show_id = %s;", [int(show_id)])
            cursor.execute("DELETE FROM zones WHERE show_id = %s;", [int(show_id)])
            cursor.execute("DELETE FROM shows WHERE id = %s;", [int(show_id)])
            conn.commit()
            self.send_json({"success": True, "message": "تم حذف العرض المسرحي بنجاح"})
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_register_device(self, body):
        device_id = body.get("id")
        device_name = body.get("deviceName")

        if not device_id or not device_name:
            self.send_json({"error": "Missing required fields"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO devices (id, device_name) 
                VALUES (%s::uuid, %s) 
                ON CONFLICT (id) DO UPDATE SET device_name = EXCLUDED.device_name;
                """,
                [str(device_id), device_name]
            )
            conn.commit()
            self.send_json({"success": True, "message": "Device registered successfully"})
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_print_ticket(self, body):
        show_id = body.get("showId")
        zone_name = body.get("zoneName")
        device_id = body.get("deviceId")
        try:
            count = int(body.get("count", 1))
        except (ValueError, TypeError):
            count = 1
        if count < 1:
            count = 1

        if not show_id or not zone_name or not device_id:
            self.send_json({"error": "Missing showId, zoneName, or deviceId"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Concurrency Row-level Lock
            cursor.execute(
                """
                SELECT z.id, z.available_seats, z.total_capacity, s.name as show_name, s.prefix as show_prefix, s.date as show_date, s.time as show_time, s.end_time as show_end_time
                FROM zones z
                JOIN shows s ON s.id = z.show_id
                WHERE z.show_id = %s AND z.zone_name = %s
                FOR UPDATE;
                """,
                [show_id, zone_name]
            )
            
            row = cursor.fetchone()
            if not row:
                self.send_json({"error": "Show zone not found"}, 404)
                conn.rollback()
                return

            zone_id, available_seats, total_capacity, show_name, show_prefix, show_date, show_time, show_end_time = row
            
            if available_seats <= 0:
                self.send_json({"error": "No seats are available in this zone"}, 400)
                conn.rollback()
                return

            if available_seats < count:
                self.send_json({"error": f"المقاعد المتبقية ({available_seats}) أقل من العدد المطلوب ({count})"}, 400)
                conn.rollback()
                return

            start_ticket_number = total_capacity - available_seats + 1
            
            # Decrement seat count by count
            cursor.execute(
                "UPDATE zones SET available_seats = available_seats - %s WHERE id = %s;",
                [count, zone_id]
            )
            
            # Format date representation safely
            try:
                formatted_date = show_date.strftime("%Y-%m-%d")
            except:
                formatted_date = str(show_date)

            # Zone digit mapping: A:1, B:2, C:3, D:4, etc.
            zone_clean = str(zone_name).strip().upper()
            if zone_clean and 'A' <= zone_clean[0] <= 'Z':
                zone_digit = str(ord(zone_clean[0]) - ord('A') + 1)
            elif zone_clean and zone_clean[0].isdigit():
                zone_digit = zone_clean[0]
            else:
                zone_digit = '1'

            tickets = []
            for i in range(count):
                curr_ticket_num = start_ticket_number + i
                # Format: Zone - Prefix + ZoneDigit + 3-digit sequence (e.g. A - 111005)
                prefix_str = str(show_prefix or "").strip()
                formatted_num = f"{prefix_str}{zone_digit}{curr_ticket_num:03d}"
                full_ticket_id = f"{zone_name} - {formatted_num}"
                passcode = generate_ticket_passcode()

                # Log print action with passcode
                cursor.execute(
                    """
                    INSERT INTO ticket_logs (show_id, zone_id, device_id, action, ticket_number, passcode)
                    VALUES (%s, %s, %s::uuid, 'PRINTED', %s, %s);
                    """,
                    [show_id, zone_id, str(device_id), curr_ticket_num, passcode]
                )
                tickets.append({
                    "showName": show_name,
                    "prefix": show_prefix or "",
                    "date": formatted_date,
                    "time": show_time,
                    "endTime": show_end_time or "",
                    "zoneName": zone_name,
                    "ticketNumber": curr_ticket_num,
                    "ticketDigits": formatted_num,
                    "ticketId": full_ticket_id,
                    "passcode": passcode
                })
            
            conn.commit()

            self.send_json({
                "success": True,
                "tickets": tickets,
                "ticket": tickets[0] if tickets else None
            })
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Transaction failed: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_update_zone(self, body):
        zone_id = body.get("zoneId")
        capacity = body.get("capacity")
        available_seats = body.get("availableSeats")

        if zone_id is None or capacity is None or available_seats is None:
            self.send_json({"error": "Missing zoneId, capacity, or availableSeats"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE zones 
                SET total_capacity = %s, available_seats = %s 
                WHERE id = %s;
                """,
                [int(capacity), int(available_seats), int(zone_id)]
            )
            conn.commit()
            self.send_json({"success": True, "message": "Zone updated successfully"})
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_clear_logs(self, body):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE ticket_logs RESTART IDENTITY;")
            conn.commit()
            self.send_json({"success": True, "message": "All print logs cleared successfully"})
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_refill_all_seats(self, body=None):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE zones SET available_seats = total_capacity;")
            conn.commit()
            self.send_json({"success": True, "message": "تمت إعادة ملء جميع مقاعد العروض بنجاح"})
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_get_logs(self):
        conn = None
        try:
            conn = get_db_connection()
            logs = query_as_dicts(
                conn,
                """
                SELECT l.id, s.name as show_name, s.prefix as show_prefix, z.zone_name, d.device_name, l.action, l.ticket_number, l.printed_at
                FROM ticket_logs l
                JOIN shows s ON s.id = l.show_id
                JOIN zones z ON z.id = l.zone_id
                LEFT JOIN devices d ON d.id = l.device_id
                ORDER BY l.printed_at DESC
                LIMIT 200;
                """
            )
            for log in logs:
                z_name = log.get('zone_name') or 'A'
                z_digit = str(ord(z_name[0]) - ord('A') + 1) if ('A' <= z_name[0] <= 'Z') else '1'
                prefix = log.get('show_prefix') or ''
                t_num = int(log.get('ticket_number') or 0)
                log['formatted_ticket_id'] = f"{z_name} - {prefix}{z_digit}{t_num:03d}"
            
            self.send_json(logs)
        except Exception as e:
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_get_gate_stats(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Total Printed
            cursor.execute("SELECT COUNT(*) FROM ticket_logs WHERE action = 'PRINTED';")
            total_printed = cursor.fetchone()[0] or 0
            
            # Total Entered
            cursor.execute("SELECT COUNT(*) FROM ticket_logs WHERE action = 'ENTERED';")
            total_entered = cursor.fetchone()[0] or 0
            
            # Recent Entrance Logs
            recent_logs = query_as_dicts(
                conn,
                """
                SELECT l.id, s.name as show_name, s.prefix as show_prefix, z.zone_name, 
                       d.device_name, l.action, l.ticket_number, l.printed_at
                FROM ticket_logs l
                JOIN shows s ON s.id = l.show_id
                JOIN zones z ON z.id = l.zone_id
                LEFT JOIN devices d ON d.id = l.device_id
                WHERE l.action = 'ENTERED'
                ORDER BY l.printed_at DESC
                LIMIT 20;
                """
            )
            
            self.send_json({
                "totalPrinted": total_printed,
                "totalEntered": total_entered,
                "recentAdmissions": recent_logs
            })
        except Exception as e:
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_verify_ticket(self, body):
        code_input = str(body.get("code") or "").strip()
        device_id = body.get("deviceId")
        if not device_id:
            device_id = str(uuid.uuid4())

        if not code_input:
            self.send_json({
                "success": False,
                "status": "INVALID",
                "message": "يرجى إدخال أو مسح كود التذكرة",
                "code": ""
            }, 400)
            return

        parsed = parse_ticket_code(code_input)
        if not parsed:
            self.send_json({
                "success": False,
                "status": "INVALID",
                "message": "كود التذكرة غير صالح أو تعذر قراءته",
                "code": code_input
            })
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 1. Find Show
            show_id = None
            show_name = None
            show_prefix = parsed["show_prefix"]
            show_date = None
            show_time = None
            show_end_time = None

            if show_prefix:
                cursor.execute(
                    "SELECT id, name, prefix, date, time, end_time FROM shows WHERE prefix = %s LIMIT 1;",
                    [show_prefix]
                )
                show_row = cursor.fetchone()
                if show_row:
                    show_id, show_name, show_prefix, show_date, show_time, show_end_time = show_row

            # If show not found by prefix, fallback search from printed logs
            if not show_id:
                cursor.execute(
                    """
                    SELECT s.id, s.name, s.prefix, s.date, s.time, s.end_time 
                    FROM ticket_logs l
                    JOIN shows s ON s.id = l.show_id
                    JOIN zones z ON z.id = l.zone_id
                    WHERE z.zone_name = %s AND l.ticket_number = %s AND l.action = 'PRINTED'
                    ORDER BY l.printed_at DESC LIMIT 1;
                    """,
                    [parsed["zone_name"], parsed["ticket_number"]]
                )
                show_row = cursor.fetchone()
                if show_row:
                    show_id, show_name, show_prefix, show_date, show_time, show_end_time = show_row

            if not show_id:
                self.send_json({
                    "success": False,
                    "status": "INVALID",
                    "message": "تذكرة غير صالحة - لم يتم العثور على العرض المسرحي",
                    "code": code_input
                })
                return

            # 2. Find Zone
            cursor.execute(
                "SELECT id, zone_name FROM zones WHERE show_id = %s AND zone_name = %s LIMIT 1;",
                [show_id, parsed["zone_name"]]
            )
            zone_row = cursor.fetchone()
            if not zone_row:
                self.send_json({
                    "success": False,
                    "status": "INVALID",
                    "message": f"تذكرة غير صالحة - المنطقة ({parsed['zone_name']}) غير مسجلة لهذا العرض",
                    "code": code_input
                })
                return

            zone_id, zone_name = zone_row
            ticket_num = parsed["ticket_number"]

            try:
                formatted_date = show_date.strftime("%Y-%m-%d")
            except:
                formatted_date = str(show_date)

            zone_digit = str(ord(zone_name[0]) - ord('A') + 1) if ('A' <= zone_name[0] <= 'Z') else '1'
            formatted_ticket_id = f"{zone_name} - {show_prefix}{zone_digit}{ticket_num:03d}"

            ticket_info = {
                "showName": show_name,
                "showPrefix": show_prefix,
                "showDate": formatted_date,
                "showTime": show_time,
                "showEndTime": show_end_time or "",
                "zoneName": zone_name,
                "ticketNumber": ticket_num,
                "ticketId": formatted_ticket_id
            }

            # 3. Check if ticket was PRINTED (sold)
            cursor.execute(
                """
                SELECT id, printed_at FROM ticket_logs 
                WHERE show_id = %s AND zone_id = %s AND ticket_number = %s AND action = 'PRINTED'
                LIMIT 1;
                """,
                [show_id, zone_id, ticket_num]
            )
            printed_row = cursor.fetchone()
            if not printed_row:
                self.send_json({
                    "success": False,
                    "status": "INVALID",
                    "message": "تذكرة غير صالحة - لم يتم بيع أو طباعة هذه التذكرة من قبل!",
                    "code": code_input,
                    "ticket": ticket_info
                })
                return

            # 4. Check if ticket is for the CURRENT ACTIVE SHOW TIME
            active_show_id = body.get("activeShowId")
            if not active_show_id:
                self.send_json({
                    "success": False,
                    "status": "INVALID",
                    "message": "يرجى اختيار العرض المطلوب مسح تذاكره من قائمة البوابة أعلى الصفحة",
                    "code": code_input,
                    "ticket": ticket_info
                })
                return

            try:
                active_show_id_int = int(active_show_id)
                if show_id != active_show_id_int:
                    cursor.execute("SELECT id, name, prefix, date, time, end_time FROM shows WHERE id = %s LIMIT 1;", [active_show_id_int])
                    target_show_row = cursor.fetchone()
                    target_show_info = None
                    if target_show_row:
                        try:
                            t_date = target_show_row[3].strftime("%Y-%m-%d")
                        except:
                            t_date = str(target_show_row[3])
                        target_show_info = {
                            "id": target_show_row[0],
                            "name": target_show_row[1],
                            "prefix": target_show_row[2],
                            "date": t_date,
                            "time": target_show_row[4],
                            "endTime": target_show_row[5] or ""
                        }
                    self.send_json({
                        "success": False,
                        "status": "WRONG_SHOW",
                        "message": f"تنبيه: هذه التذكرة مخصصة لعرض آخر ({show_name}) وليست لهذا العرض!",
                        "code": code_input,
                        "ticket": ticket_info,
                        "targetShow": target_show_info
                    })
                    return
            except (ValueError, TypeError):
                pass

            # 5. Check if ticket was ALREADY ENTERED
            cursor.execute(
                """
                SELECT l.id, l.printed_at, d.device_name 
                FROM ticket_logs l
                LEFT JOIN devices d ON d.id = l.device_id
                WHERE l.show_id = %s AND l.zone_id = %s AND l.ticket_number = %s AND l.action = 'ENTERED'
                ORDER BY l.printed_at ASC LIMIT 1;
                """,
                [show_id, zone_id, ticket_num]
            )
            entered_row = cursor.fetchone()
            if entered_row:
                entered_time_str = entered_row[1].strftime("%Y-%m-%d %I:%M:%S %p") if hasattr(entered_row[1], 'strftime') else str(entered_row[1])
                gate_name = entered_row[2] or "البوابة الإلكترونية"
                self.send_json({
                    "success": False,
                    "status": "ALREADY_ENTERED",
                    "message": "تنبيه: تم الدخول بهذه التذكرة مسبقاً!",
                    "code": code_input,
                    "firstEnteredAt": entered_time_str,
                    "gateDeviceName": gate_name,
                    "ticket": ticket_info
                })
                return

            # 6. Record Valid Entrance Admission
            cursor.execute(
                """
                INSERT INTO ticket_logs (show_id, zone_id, device_id, action, ticket_number)
                VALUES (%s, %s, %s::uuid, 'ENTERED', %s);
                """,
                [show_id, zone_id, str(device_id), ticket_num]
            )
            conn.commit()

            now_str = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

            self.send_json({
                "success": True,
                "status": "VALID",
                "message": "تذكرة صالحة ومؤكدة - مصرح بالدخول",
                "code": code_input,
                "admittedAt": now_str,
                "ticket": ticket_info
            })
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            self.send_json({"error": "Verification error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_user_ticket_login(self, body):
        ticket_digits_input = str(body.get("ticketDigits") or body.get("username") or "").strip().strip('*').strip()
        passcode_input = str(body.get("passcode") or body.get("password") or "").strip().upper()

        if not ticket_digits_input or not passcode_input:
            self.send_json({"error": "يرجى إدخال رقم التذكرة (اسم المستخدم) وكلمة المرور"}, 400)
            return

        # Parse digits or full ticket ID using parse_ticket_code
        parsed = parse_ticket_code(ticket_digits_input)
        if not parsed:
            self.send_json({"error": "رقم التذكرة غير صالح"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Find show
            show_id = None
            show_name = None
            show_prefix = parsed["show_prefix"]
            show_date = None
            show_time = None

            if show_prefix:
                cursor.execute(
                    "SELECT id, name, prefix, date, time, end_time FROM shows WHERE prefix = %s LIMIT 1;",
                    [show_prefix]
                )
                row = cursor.fetchone()
                if row:
                    show_id, show_name, show_prefix, show_date, show_time, show_end_time = row

            if not show_id:
                # Try finding from ticket_logs
                cursor.execute(
                    """
                    SELECT s.id, s.name, s.prefix, s.date, s.time, s.end_time 
                    FROM ticket_logs l
                    JOIN shows s ON s.id = l.show_id
                    JOIN zones z ON z.id = l.zone_id
                    WHERE z.zone_name = %s AND l.ticket_number = %s AND l.action = 'PRINTED'
                    ORDER BY l.printed_at DESC LIMIT 1;
                    """,
                    [parsed["zone_name"], parsed["ticket_number"]]
                )
                row = cursor.fetchone()
                if row:
                    show_id, show_name, show_prefix, show_date, show_time, show_end_time = row

            if not show_id:
                self.send_json({"error": "العرض المسرحي غير موجود أو كود العرض غير صحيح"}, 404)
                return

            # Find zone
            cursor.execute(
                "SELECT id, zone_name FROM zones WHERE show_id = %s AND zone_name = %s LIMIT 1;",
                [show_id, parsed["zone_name"]]
            )
            zone_row = cursor.fetchone()
            if not zone_row:
                self.send_json({"error": "المنطقة المحددة غير صالحة لهذا العرض"}, 404)
                return

            zone_id, zone_name = zone_row
            ticket_num = parsed["ticket_number"]

            # Query ticket_logs for action = 'PRINTED'
            cursor.execute(
                """
                SELECT id, passcode, printed_at FROM ticket_logs 
                WHERE show_id = %s AND zone_id = %s AND ticket_number = %s AND action = 'PRINTED'
                ORDER BY printed_at DESC LIMIT 1;
                """,
                [show_id, zone_id, ticket_num]
            )
            ticket_log = cursor.fetchone()
            if not ticket_log:
                self.send_json({"error": "لم يتم العثور على تذكرة مباعة بهذا الرقم"}, 404)
                return

            saved_passcode = str(ticket_log[1] or "").strip().upper()
            
            # Check passcode match
            if saved_passcode and saved_passcode != passcode_input:
                self.send_json({"error": "كلمة المرور غير صحيحة، يرجى التأكد من الرمز المطبوع أسفل التذكرة"}, 401)
                return

            try:
                formatted_date = show_date.strftime("%Y-%m-%d")
            except:
                formatted_date = str(show_date)

            zone_clean = str(zone_name).strip().upper()
            zone_digit = str(ord(zone_clean[0]) - ord('A') + 1) if ('A' <= zone_clean[0] <= 'Z') else '1'
            formatted_num = f"{show_prefix}{zone_digit}{ticket_num:03d}"
            full_ticket_id = f"{zone_name} - {formatted_num}"

            self.send_json({
                "success": True,
                "ticket": {
                    "showName": show_name,
                    "showPrefix": show_prefix or "",
                    "showDate": formatted_date,
                    "showTime": show_time,
                    "showEndTime": show_end_time or "",
                    "zoneName": zone_name,
                    "zoneDigit": zone_digit,
                    "ticketNumber": ticket_num,
                    "ticketDigits": formatted_num,
                    "ticketId": full_ticket_id,
                    "passcode": saved_passcode or passcode_input,
                    "printedAt": ticket_log[2].isoformat() if hasattr(ticket_log[2], 'isoformat') else str(ticket_log[2])
                }
            })
        except Exception as e:
            self.send_json({"error": "Authentication error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_auth_login(self, body):
        username = str(body.get("username") or "").strip().lower()
        password = str(body.get("password") or "").strip()

        if not username or not password:
            self.send_json({"error": "يرجى إدخال اسم المستخدم وكلمة المرور"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, password_hash, full_name, role, is_active FROM users WHERE LOWER(username) = %s LIMIT 1;",
                [username]
            )
            row = cursor.fetchone()
            if not row:
                self.send_json({"error": "اسم المستخدم أو كلمة المرور غير صحيحة"}, 401)
                return

            user_id, u_name, pwd_hash, full_name, role, is_active = row
            if not is_active:
                self.send_json({"error": "تم تعطيل هذا الحساب. يرجى التواصل مع مدير النظام"}, 403)
                return

            if not verify_password(password, pwd_hash):
                self.send_json({"error": "اسم المستخدم أو كلمة المرور غير صحيحة"}, 401)
                return

            self.send_json({
                "success": True,
                "user": {
                    "id": user_id,
                    "username": u_name,
                    "fullName": full_name,
                    "role": role
                }
            })
        except Exception as e:
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_get_users(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, full_name, role, is_active, created_at FROM users ORDER BY id ASC;"
            )
            rows = cursor.fetchall()
            users = []
            for r in rows:
                users.append({
                    "id": r[0],
                    "username": r[1],
                    "fullName": r[2],
                    "role": r[3],
                    "isActive": r[4],
                    "createdAt": r[5].isoformat() if hasattr(r[5], 'isoformat') else str(r[5])
                })
            self.send_json(users)
        except Exception as e:
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_create_user(self, body):
        username = str(body.get("username") or "").strip().lower()
        password = str(body.get("password") or "").strip()
        full_name = str(body.get("fullName") or "").strip()
        role = str(body.get("role") or "ticket_seller").strip().lower()

        if not username or not password or not full_name:
            self.send_json({"error": "يرجى تعبئة كافة الحقول المطلوبة (اسم المستخدم، الاسم الكامل، كلمة المرور)"}, 400)
            return

        if role not in ('scanner', 'ticket_seller', 'admin', 'superuser'):
            self.send_json({"error": "صلاحية غير صالحة"}, 400)
            return

        if len(password) < 4:
            self.send_json({"error": "يجب ألا تقل كلمة المرور عن 4 أحرف/أرقام"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE LOWER(username) = %s LIMIT 1;", [username])
            if cursor.fetchone():
                self.send_json({"error": "اسم المستخدم هذا مسجل بالفعل. يرجى اختيار اسم مستخدم آخر"}, 400)
                return

            pwd_hash = hash_password(password)
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                [username, pwd_hash, full_name, role]
            )
            new_id = cursor.fetchone()[0]
            conn.commit()

            self.send_json({
                "success": True,
                "user": {
                    "id": new_id,
                    "username": username,
                    "fullName": full_name,
                    "role": role
                }
            })
        except Exception as e:
            if conn: conn.rollback()
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_delete_user(self, body):
        user_id = body.get("userId")
        if not user_id:
            self.send_json({"error": "Missing userId"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Check user role and total superusers
            cursor.execute("SELECT id, username, role FROM users WHERE id = %s;", [user_id])
            target_user = cursor.fetchone()
            if not target_user:
                self.send_json({"error": "المستخدم غير موجود"}, 404)
                return

            if target_user[2] == 'superuser':
                cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'superuser';")
                super_count = cursor.fetchone()[0]
                if super_count <= 1:
                    self.send_json({"error": "لا يمكن حذف مدير النظام الوحيد في البرنامج"}, 400)
                    return

            cursor.execute("DELETE FROM users WHERE id = %s;", [user_id])
            conn.commit()
            self.send_json({"success": True})
        except Exception as e:
            if conn: conn.rollback()
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

    def handle_change_password(self, body):
        user_id = body.get("userId")
        new_password = str(body.get("newPassword") or "").strip()

        if not user_id or not new_password:
            self.send_json({"error": "Missing userId or newPassword"}, 400)
            return

        if len(new_password) < 4:
            self.send_json({"error": "يجب ألا تقل كلمة المرور عن 4 أحرف/أرقام"}, 400)
            return

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            pwd_hash = hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s;", [pwd_hash, user_id])
            conn.commit()
            self.send_json({"success": True})
        except Exception as e:
            if conn: conn.rollback()
            self.send_json({"error": "Database error: " + str(e)}, 500)
        finally:
            if conn:
                conn.close()

def init_db_schema():
    """Ensure users table exists and default superuser is created."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(150) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'ticket_seller',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            ALTER TABLE shows ADD COLUMN IF NOT EXISTS is_gate_active BOOLEAN DEFAULT TRUE;
            UPDATE shows SET is_gate_active = TRUE WHERE is_gate_active IS NULL;
        """)
        # Check if any superuser exists
        cursor.execute("SELECT id FROM users LIMIT 1;")
        if not cursor.fetchone():
            default_pwd = hash_password("admin123")
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (%s, %s, %s, %s);
            """, ["admin", default_pwd, "مدير النظام", "superuser"])
            conn.commit()
            print("Initialized default superuser account: username='admin', password='admin123'")
        else:
            conn.commit()
    except Exception as e:
        print(f"Error initializing DB users schema: {e}")
    finally:
        if conn:
            conn.close()

def run_server():
    init_db_schema()
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, TheatreHTTPHandler)
    print(f"Theatre ticketing backend running on port {PORT} (Pure Python Native Server)...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run_server()
