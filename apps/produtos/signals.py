from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import VariacaoProduto
import barcode
from barcode.writer import ImageWriter
import qrcode
from django.core.files import File
from io import BytesIO

@receiver(pre_save, sender=VariacaoProduto)
def check_codigo_barras_change(sender, instance, **kwargs):
    """Verifica se o código de barras mudou antes de salvar."""
    if instance.pk:  # Se é uma atualização
        old_instance = VariacaoProduto.objects.get(pk=instance.pk)
        instance._codigo_barras_changed = instance.codigo_barras != old_instance.codigo_barras
    else:  # Se é uma criação
        instance._codigo_barras_changed = True if instance.codigo_barras else False

@receiver(post_save, sender=VariacaoProduto)
def gerar_codigos_produto(sender, instance, created, **kwargs):
    """
    Gera ou atualiza a imagem do código de barras e o QR code após salvar o VariacaoProduto,
    se o campo codigo_barras estiver preenchido ou tiver sido alterado.
    """
    if hasattr(instance, '_codigo_barras_changed') and instance._codigo_barras_changed and instance.codigo_barras:
        codigo = instance.codigo_barras.strip()
        barcode_type = None

        # Detecta o padrão do código de barras com base no tamanho e conteúdo
        if len(codigo) == 13 and codigo.isdigit():
            barcode_type = 'ean13'
        elif len(codigo) == 8 and codigo.isdigit():
            barcode_type = 'ean8'
        elif len(codigo) == 12 and codigo.isdigit():
            barcode_type = 'upca'
        else:
            barcode_type = 'code128'  # Padrão variável para outros tamanhos

        # Remove imagens antigas, se existirem
        if instance.barcode_image:
            instance.barcode_image.delete(save=False)
        if instance.qr_code:
            instance.qr_code.delete(save=False)

        # Gera a imagem do código de barras
        try:
            barcode_class = barcode.get_barcode_class(barcode_type)
            bc = barcode_class(codigo, writer=ImageWriter())
            buffer = BytesIO()
            bc.write(buffer)
            instance.barcode_image.save(f'barcode_{codigo}.png', File(buffer), save=False)
            buffer.close()
        except Exception as e:
            print(f"Erro ao gerar código de barras ({barcode_type}): {e}")

        # Gera o QR code
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(codigo)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            instance.qr_code.save(f'qrcode_{codigo}.png', File(buffer), save=False)
            buffer.close()
        except Exception as e:
            print(f"Erro ao gerar QR code: {e}")

        # Salva as alterações sem disparar o signal novamente
        instance.save(update_fields=['barcode_image', 'qr_code'])