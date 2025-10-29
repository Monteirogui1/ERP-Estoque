import os
import sys
try:
    import win32event
    import win32service
    import win32serviceutil
    import servicemanager
except ImportError as e:
    print(f"Erro ao importar módulos do pywin32: {e}")
    sys.exit(1)
from subprocess import Popen

class DjangoService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DjangoERPService"
    _svc_display_name_ = "ERP Frota Django Service"
    _svc_description_ = "Serviço para executar o sistema ERP Frota com Django e Waitress em produção."

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.process:
            self.process.terminate()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        # Caminho para o Python e o projeto Django
        python_path = r"C:\Python310\python.exe"  # Ajuste se usar ambiente virtual
        project_path = r"C:\App python\ERP-Estoque"

        # Configura o ambiente Django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

        # Comando para executar o Waitress
        command = [
            python_path,
            "-m", "waitress",
            "--host", "192.168.100.243",
            "--port", "8002",
            "core.wsgi:application"
        ]

        # Cria o diretório de logs, se não existir
        log_dir = os.path.join(project_path, "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Inicia o Waitress em segundo plano
        self.process = Popen(
            command,
            stdout=open(os.path.join(log_dir, "waitress.log"), "a"),
            stderr=open(os.path.join(log_dir, "waitress_error.log"), "a"),
            creationflags=0x08000000,  # Executa em segundo plano
            cwd=project_path
        )

        # Aguarda o sinal de parada do serviço
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DjangoService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(DjangoService)