from django.views import View
from django.shortcuts import render, redirect
from .forms import ClienteWizardForm
from .models import Cliente
from django.contrib.auth.models import User
import subprocess
from django.contrib import messages

class ClienteWizardView(View):
    template_name = 'shared/cliente_wizard.html'

    def get(self, request):
        form = ClienteWizardForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ClienteWizardForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            db_name = cliente.banco
            # 1. Cria o banco físico (Postgres exemplo)
            subprocess.run(['createdb', db_name])  # Ajuste para seu SGBD
            cliente.save()

            # 2. Roda migrações no novo banco
            subprocess.run(['python', 'manage.py', 'migrate', '--database', db_name])

            # 3. Cria usuário admin inicial, se fornecido
            if form.cleaned_data.get('email_admin') and form.cleaned_data.get('senha_admin'):
                # Criação temporária no banco novo
                from django.db import connections
                from django.contrib.auth.hashers import make_password
                with connections[db_name].cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO auth_user (username, email, is_staff, is_superuser, is_active, password, date_joined) "
                        "VALUES (%s, %s, TRUE, TRUE, TRUE, %s, now())",
                        [
                            'admin',
                            form.cleaned_data['email_admin'],
                            make_password(form.cleaned_data['senha_admin'])
                        ]
                    )
            messages.success(request, f'Cliente {cliente.nome} criado e banco {db_name} provisionado!')
            return redirect('admin:shared_cliente_changelist')
        return render(request, self.template_name, {'form': form})
