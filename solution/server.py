from http.server import HTTPServer,BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs,urlparse

compras={}

#existen dos tipos fisco y digital
class Compra:
    def __init__(self,client,status,payment,order_type):
        self.client=client
        self.status=status
        self.payment=payment
        self.order_type=order_type

class Fisico(Compra):
    def __init__(self, client, status, payment, shipping, products):
        super().__init__( client, status, payment,"Fisica")
        self.shipping=shipping
        self.products=products

class Digital(Compra):
    def __init__(self, client, status, payment, code, expiration):
        super().__init__(client, status, payment,"Digital")
        self.code=code
        self.expiration=expiration

class CompraFactory:
    @staticmethod
    def create_compra(order_type,client,status,payment,shipping,products,code,expiration):
        if order_type=="Fisica":
            return Fisico(client,status,payment,shipping,products)
        elif order_type=="Digital":
            return Digital(client,status,payment,code,expiration)
        else:
            raise ValueError("Tipo de compra no valida")
        
class CompraService:
    def __init__(self):
        self.factory=CompraFactory()

    def add_compra(self,data):
        order_type=data.get('order_type',None)
        client=data.get('client',None)
        status=data.get('status',None)
        payment=data.get('payment',None)
        shipping=data.get('shipping',None)
        products=data.get('products',None)
        code=data.get('code',None)
        expiration=data.get('expiration',None)
        nuevo=self.factory.create_compra(order_type,client,status,payment,shipping,products,code,expiration)
        if not compras:
            compras[1]=nuevo
        else:
            id=max(compras.keys())+1
            compras[id]=nuevo
        return nuevo.__dict__
    
    def read_compras(self):
        return {index:compra.__dict__ for index,compra in compras.items()}

    def buscar_status(self,status):
        n={}
        lista=self.read_compras().items()
        for i, j in lista:
            if j['status']==status:
                n[i]=j
        return n
    
    def actualizar_id(self,id,data):
        status=data.get('status',None)
        lista=self.read_compras().items()
        for i, j in lista:
            if i==id:
                j['status']=status
                return j
        return None
    
    def eliminar_id(self,id):
        lista=self.read_compras().items()
        for i,j in lista:
            if i==id:
                del compras[i]
                return {"message":"Orden eliminada"}
        return None
                


class HTTPResponseHandler:
    @staticmethod
    def response_handler(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-Type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))

    @staticmethod
    def read_data(handler):
        content_length=int(handler.headers['Content-Length'])
        data=handler.rfile.read(content_length)
        return json.loads(data.decode('utf-8'))
    
class CompraHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller=CompraService()
        super().__init__(*args,**kwargs)

    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        if parsed_path.path=="/orders/":
            if 'status' in query_params:
                status=query_params['status'][0]
                busca=self.controller.buscar_status(status)
                if busca:
                    HTTPResponseHandler.response_handler(self,200,busca)
                else:
                    HTTPResponseHandler.response_handler(self,404,{"Error":"No existe el estado"})
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
        elif parsed_path.path=="/orders":
            HTTPResponseHandler.response_handler(self,200,self.controller.read_compras())
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})
        

    def do_POST(self):
        if self.path=="/orders":
            data=HTTPResponseHandler.read_data(self)
            compra_c=self.controller.add_compra(data)
            HTTPResponseHandler.response_handler(self,201,compra_c)
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/orders/"):
            id=int(self.path.split("/")[-1])
            data=HTTPResponseHandler.read_data(self)            
            compra_act=self.controller.actualizar_id(id,data)
            if compra_act:
                HTTPResponseHandler.response_handler(self,200,compra_act)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encontrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/orders/"):
            id=int(self.path.split("/")[-1])
            borrado=self.controller.eliminar_id(id)
            if borrado:
                HTTPResponseHandler.response_handler(self,200,borrado)
            else:
                HTTPResponseHandler.response_handler(self,404,{"Error":"ID no encotrado"})
        else:
            HTTPResponseHandler.response_handler(self,404,{"Error":"Ruta no encontrada"})


            

def main(port=8000):

    try:
        server_adress=('',port)
        httpd=HTTPServer(server_adress,CompraHandler)
        print(f'Iniciando el servidor en el puerto {port}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando el servidor...")
        httpd.socket.close()

if __name__ == "__main__":
    main()

