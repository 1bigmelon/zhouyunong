from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    import os
    from app.models.User import User, encrypt
    from app.models.Base import Base
    if not os.path.exists('.init'):
        Base.objects().delete()
        u = User.get_or_create('DogAdmin', name='测试用狗管理', password=encrypt('1145141919810'))
        u.authority = 0x1110
        u.save_changes()
        with open('.init', 'w') as f: pass
    flask_app.run('0.0.0.0')
