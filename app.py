from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'entrar'

# Modelo de Usuário
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Modelo de Cliente AnyDesk
class AnyDeskClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    anydesk_id = db.Column(db.String(20), nullable=False)
    anydesk_password = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas de Autenticação
@app.route('/')
def index():
    return redirect(url_for('entrar'))

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('painel_admin'))
            return redirect(url_for('painel_usuario'))
        flash('Usuário ou senha inválidos')
    return render_template('entrar.html')

@app.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('entrar'))

# Rotas do Admin
@app.route('/admin')
@login_required
def painel_admin():
    if not current_user.is_admin:
        return redirect(url_for('painel_usuario'))
    return render_template('painel_admin.html')

@app.route('/admin/usuarios')
@login_required
def gerenciar_usuarios():
    if not current_user.is_admin:
        return redirect(url_for('painel_usuario'))
    users = User.query.all()
    return render_template('gerenciar_usuarios.html', users=users)

@app.route('/admin/usuarios/adicionar', methods=['POST'])
@login_required
def adicionar_usuario():
    if not current_user.is_admin:
        return redirect(url_for('painel_usuario'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'
    
    if User.query.filter_by(username=username).first():
        flash('Usuário já existe')
        return redirect(url_for('gerenciar_usuarios'))
    
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        is_admin=is_admin
    )
    db.session.add(user)
    db.session.commit()
    flash('Usuário adicionado com sucesso')
    return redirect(url_for('gerenciar_usuarios'))

@app.route('/admin/usuarios/<int:user_id>/excluir', methods=['POST'])
@login_required
def excluir_usuario(user_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Não autorizado'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'error': 'Não é possível excluir seu próprio usuário'}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuário excluído com sucesso'})

# Rotas do Usuário
@app.route('/usuario')
@login_required
def painel_usuario():
    return render_template('painel_usuario.html')

# Rotas do AnyDesk
@app.route('/anydesk')
@login_required
def clientes_anydesk():
    clients = AnyDeskClient.query.all()
    return render_template('clientes_anydesk.html', clients=clients)

@app.route('/anydesk/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_cliente_anydesk():
    if request.method == 'POST':
        client = AnyDeskClient(
            client_name=request.form.get('client_name'),
            anydesk_id=request.form.get('anydesk_id'),
            anydesk_password=request.form.get('anydesk_password')
        )
        db.session.add(client)
        db.session.commit()
        flash('Cliente AnyDesk adicionado com sucesso')
        return redirect(url_for('clientes_anydesk'))
    return render_template('adicionar_cliente_anydesk.html')

@app.route('/anydesk/<int:client_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cliente_anydesk(client_id):
    client = AnyDeskClient.query.get_or_404(client_id)
    if request.method == 'POST':
        client.client_name = request.form.get('client_name')
        client.anydesk_id = request.form.get('anydesk_id')
        client.anydesk_password = request.form.get('anydesk_password')
        db.session.commit()
        flash('Cliente AnyDesk atualizado com sucesso')
        return redirect(url_for('clientes_anydesk'))
    return render_template('adicionar_cliente_anydesk.html', client=client)

@app.route('/anydesk/<int:client_id>/excluir', methods=['POST'])
@login_required
def excluir_cliente_anydesk(client_id):
    client = AnyDeskClient.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Cliente AnyDesk excluído com sucesso'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Criar usuário admin se não existir
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    app.run(host='0.0.0.0', debug=True) 