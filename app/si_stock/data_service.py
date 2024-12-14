import requests
from si_stock.models import Resumo

def get_resumo_data():
    url = 'http://0.0.0.0:8000/api/v1/si-stock/resumo/'
    
    try:
        response = requests.get(url)
        print(response.json())
    except requests.exceptions.RequestException as err:
        print(err)
    
    # data_list = response.json()
    # print(data_list)
    
    # if data_list:
    #     for data in data_list:
    #         resumo = Resumo.objects.create(
    #             provincia = data['provincia'],
    #             sector=data['sector'],
    #             instrumento=data['instrumento'],
    #             data_entrada=data['data_entrada'],
    #             quantidade=data['quantidade'],
    #             fornecedor=data['fornecedor'],
    #             stock=data['stock'],
    #             necessidade=data['necessidade'],
    #             requisicao_id=data['requisicao_id'],
    #             data_requisicao=data['data_requisicao'],
    #             quantidade_requisicao=data['quantidade_requisicao'],
    #             status_requisicao=data['status_requisicao']                
    #         )
            
    #         resumo.save()