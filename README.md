# Sistema de Carrito de Compras Django

Este proyecto es un sistema de comercio electrónico desarrollado con Django.

**Demo desplegada**: [https://ecommerce-project-z9w3.onrender.com/](https://ecommerce-project-z9w3.onrender.com/)

## Instalación y Ejecución

1.  Clonar el repositorio.
2.  Crear un entorno virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
3.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Aplicar migraciones:
    ```bash
    python manage.py migrate
    ```
5.  (Opcional) Cargar datos de prueba:
    ```bash
    python manage.py populate_db
    ```
6.  Ejecutar el servidor:
    ```bash
    python manage.py runserver
    ```

## Estructura del Proyecto

-   `config/`: Configuración principal del proyecto.
-   `store/`: Gestión de productos, categorías, reviews y wishlist.
-   `cart/`: Lógica del carrito de compras (basado en sesiones).
-   `users/`: Gestión de usuarios (registro, login, perfil, historial).
-   `orders/`: Gestión de órdenes de compra.
-   `coupons/`: Sistema de cupones de descuento.
-   `payment/`: Integración con pasarelas de pago (simulado/MercadoPago).
-   `docs/`: Documentación y diagramas (Mermaid).
-   `DEPLOYMENT.md`: Guía completa de deployment.

## Decisiones de Diseño

-   **Carrito en Sesión**: Se optó por persistir el carrito en la sesión del usuario para permitir compras sin registro previo (guest checkout) y mejorar el rendimiento.
-   **Usuarios**: Se extendió el modelo `User` de Django mediante un modelo `Profile` (OneToOne) para almacenar dirección y teléfono.
-   **Búsqueda**: Implementada con consultas `Q` para filtrar por nombre y descripción.
-   **Frontend**: Se utilizó Tailwind CSS (vía CDN) para un diseño rápido y responsive, extendiendo la plantilla base.

## Testing

Se incluyen más de 20 tests unitarios. Para ejecutarlos:
```bash
python manage.py test
```

## Production Deployment

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
MERCADOPAGO_PUBLIC_KEY=your-mercadopago-public-key
MERCADOPAGO_ACCESS_TOKEN=your-mercadopago-access-token
```

### Quick Deployment

1. **Install production dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables** (see `.env.example`)

3. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run with gunicorn**:
   ```bash
   gunicorn config.wsgi:application
   ```

### Deployment Platforms

This project is ready to deploy on:
- **Render** (recommended) - See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
- Heroku
- Railway
- DigitalOcean App Platform

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed platform-specific instructions.

### Health Check

The application includes a health check endpoint at `/health/` for monitoring.

### Security Features

- Environment-based configuration
- HTTPS/SSL enforcement in production
- Secure cookies and CSRF protection
- HSTS headers
- XSS and clickjacking protection
- Comprehensive logging

