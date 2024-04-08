import requests

url="http://localhost:8000/"

compra_new={
    "client":"Juan Perez",
    "status":"Pendiente",
    "payment":"Tarjeta de Credito",
    "shipping":10.0,
    "products":["Camiseta","Pantalon","Zapatos"],
    "order_type":"Fisica"
}
response_new=requests.post(url+"orders",json=compra_new)
print("--añadido--")
print(response_new.text)

#segundi post

compra_new={
    "client":"Maria Rodriguez",
    "status":"Pendiente",
    "payment":"Paypal",
    "code":"ABC123",
    "expiration":"2022-12-31",
    "order_type":"Digital"
}

response_new=requests.post(url+"orders",json=compra_new)
print("--añadido--")
print(response_new.text)
