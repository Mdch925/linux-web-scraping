import socket
import threading
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# إنشاء سوكيت TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(5)  # السماح بحد أقصى 5 اتصالات في نفس الوقت
secure_socket = context.wrap_socket(server_socket, server_side=True)

print("🚀Server on wait..")


# قائمة لتخزين العملاء المتصلين
clients = []


# دالة لمعالجة كل عميل في Thread منفصل
def handle_client(client_socket, addr):
    print(f"📞 new call from: {addr}")
    clients.append(client_socket)  # إضافة العميل للقائمة

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message or message.lower() == "exit":
                print(f"❌ client {addr} غادر.")
                clients.remove(client_socket)
                break

            print(f"📩 client {addr}: {message}")

            # إرسال الرسالة لجميع العملاء الآخرين
            for client in clients:
                if client != client_socket:  # ✅ تم إصلاح الخطأ هنا
                    client.send(f"{addr}: {message}".encode("utf-8"))

        except Exception as e:  # ✅ تم تحسين التعامل مع الأخطاء
            print(f"⚠️ Error with client {addr}: {e}")
            clients.remove(client_socket)
            break

    client_socket.close()


# قبول عدة اتصالات
while True:
    client_socket, addr = secure_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
