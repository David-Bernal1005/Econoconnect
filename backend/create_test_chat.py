from app.db.session import SessionLocal
from app.models.chat import Chat

def create_test_chat():
    db = SessionLocal()
    try:
        chat = db.query(Chat).filter(Chat.id_chat == 1).first()
        if not chat:
            new_chat = Chat(
                nombre='Chat de prueba',
                tipo='privado',
                creador_id=1,
                estado='activo'
            )
            db.add(new_chat)
            db.commit()
            print('Chat de prueba creado')
        else:
            print(f'Chat ya existe: id={chat.id_chat}')
    finally:
        db.close()

if __name__ == '__main__':
    create_test_chat()