from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Produto, VariacaoProduto
import barcode
from barcode.writer import ImageWriter
import qrcode
from django.core.files import File
from io import BytesIO
from django.db.models import F

@receiver(post_save, sender=VariacaoProduto)
def gerar_codigos_produto(sender, instance, created, **kwargs):
    """
    Gera a imagem do código de barras e o QR code após salvar o produto,
    apenas se o campo codigo_barras estiver preenchido e as imagens ainda não existirem.
    """
    if instance.codigo_barras:
        # Detecta o padrão do código de barras com base no tamanho e conteúdo
        codigo = instance.codigo_barras.strip()
        barcode_type = None

        if len(codigo) == 13 and codigo.isdigit():
            barcode_type = 'ean13'
        elif len(codigo) == 8 and codigo.isdigit():
            barcode_type = 'ean8'
        elif len(codigo) == 12 and codigo.isdigit():
            barcode_type = 'upca'
        else:
            barcode_type = 'code128'  # Padrão variável para outros tamanhos

        # Gera a imagem do código de barras se ainda não existe
        if not instance.barcode_image:
            try:
                barcode_class = barcode.get_barcode_class(barcode_type)
                bc = barcode_class(codigo, writer=ImageWriter())
                buffer = BytesIO()
                bc.write(buffer)
                instance.barcode_image.save(f'barcode_{codigo}.png', File(buffer), save=False)
                buffer.close()
            except Exception as e:
                print(f"Erro ao gerar código de barras ({barcode_type}): {e}")

        # Gera o QR code se ainda não existe
        if not instance.qr_code:
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

        # Se alguma imagem foi gerada, atualiza o objeto no banco sem disparar o signal novamente
        if instance.barcode_image.name or instance.qr_code.name:
            VariacaoProduto.objects.filter(pk=instance.pk).update(
                barcode_image=F('barcode_image') if instance.barcode_image.name else None,
                qr_code=F('qr_code') if instance.qr_code.name else None
            )