from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    import os
    from app.models.User import User
    if not os.path.exists('.init'):
        u = User.get_or_create('测试用狗管理', 'DogAdmin', '1145141919810')
        u.authority = 4096
        u.save()
        with open('.init', 'w') as f: pass
    flask_app.run('0.0.0.0') 
