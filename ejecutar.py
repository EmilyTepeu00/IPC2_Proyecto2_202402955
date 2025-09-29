from app import crear_app

#CREAR INSTANCIA DE LA APP Flask
app = crear_app()

if __name__ == '__main__':
    print("Iniciando Sistema de Riego Automatizado...")
    print("Aplicación disponible en: http://127.0.0.1:5000")
    print("Presione CTRL+C para detener el servidor")
    print("-" * 50)
    
    #EJECUTAR APP
    app.run(debug=True, host='127.0.0.1', port=5000)