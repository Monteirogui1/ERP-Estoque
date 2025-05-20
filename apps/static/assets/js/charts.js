document.addEventListener('DOMContentLoaded', function () {
    // Gráfico de Vendas por Categoria (Barra)
    const vendasPorCategoriaData = JSON.parse(document.getElementById('vendasPorCategoriaData').textContent);
    const vendasPorCategoriaCtx = document.getElementById('vendasPorCategoriaChart').getContext('2d');
    new Chart(vendasPorCategoriaCtx, {
        type: 'bar',
        data: {
            labels: vendasPorCategoriaData.map(item => item.categoria),
            datasets: [{
                label: 'Quantidade Vendida',
                data: vendasPorCategoriaData.map(item => item.total_vendido),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quantidade'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Categoria'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Quantidade: ${context.parsed.y}`;
                        }
                    }
                }
            }
        }
    });

    // Gráfico de Vendas por Período (Linha)
    const vendasPorPeriodoData = JSON.parse(document.getElementById('vendasPorPeriodoData').textContent);
    const vendasPorPeriodoCtx = document.getElementById('vendasPorPeriodoChart').getContext('2d');
    new Chart(vendasPorPeriodoCtx, {
        type: 'line',
        data: {
            labels: vendasPorPeriodoData.labels,
            datasets: [{
                label: 'Valor das Vendas (R$)',
                data: vendasPorPeriodoData.valores,
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Valor (R$)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Período'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `R$ ${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
});