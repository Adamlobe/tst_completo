from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Pegando os dados do formulário
    data = request.form

    # Verificando se todas as chaves esperadas estão presentes
    required_keys = ['data', 'placa', 'Freios', 'Luzes', 'Pneus', 'Oleo', 'CintoDeSeguranca',
                     'nome_empresa', 'cnpj', 'nome_assinatura']
    for key in required_keys:
        if key not in data:
            return f"Erro: Campo '{key}' está faltando no formulário.", 400

    # Criando o PDF na memória
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 750, "Checklist de Segurança de Caminhão")
    c.drawString(100, 730, f"Data: {data['data']}")
    c.drawString(100, 710, f"Placa do Caminhão: {data['placa']}")
    c.drawString(100, 690, f"Nome da Empresa: {data['nome_empresa']}")
    c.drawString(100, 670, f"CNPJ: {data['cnpj']}")

    # Exibindo os itens do checklist padrão
    default_items = ['Freios', 'Luzes', 'Pneus', 'Oleo', 'CintoDeSeguranca']
    y = 650
    for item in default_items:
        c.drawString(100, y, f"{item}: {data[item]}")
        y -= 20

    # Exibindo os itens do checklist flexíveis
    flexible_items = zip(data.getlist('item[]'), data.getlist('conforme[]'))
    for item, conforme in flexible_items:
        c.drawString(100, y, f"{item}: {conforme}")
        y -= 20

    # Adicionando campo de assinatura
    c.drawString(100, 50, f"Assinatura: {data['nome_assinatura']}")
    c.line(100, 30, 300, 30)  # Linha de assinatura

    c.save()
    pdf_buffer.seek(0)

    # Usar a placa do caminhão para nomear o arquivo PDF
    pdf_filename = f"checklist_seguranca_{data['placa']}.pdf"

    return send_file(pdf_buffer, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)