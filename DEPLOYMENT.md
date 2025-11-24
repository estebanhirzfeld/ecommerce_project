# Production Deployment Guide

This guide provides step-by-step instructions for deploying the Django e-commerce application to production.

## Prerequisites

- Python 3.11+
- PostgreSQL database (optional, SQLite works for smaller deployments)
- Git repository
- Account on deployment platform (Heroku, Railway, Render, etc.)

## Environment Variables

Create a `.env` file with the following variables (see `.env.example` for template):

```bash
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
MERCADOPAGO_PUBLIC_KEY=your-mercadopago-public-key
MERCADOPAGO_ACCESS_TOKEN=your-mercadopago-access-token
```

### Generating a Secret Key

Generate a new secret key for production:

```python
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deployment Platforms

### Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
   heroku config:set MERCADOPAGO_PUBLIC_KEY="your-key"
   heroku config:set MERCADOPAGO_ACCESS_TOKEN="your-token"
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Run migrations**:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

6. **Collect static files** (automatic with whitenoise):
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

### Railway

1. **Install Railway CLI** or use the web interface

2. **Create new project** and link repository

3. **Set environment variables** in Railway dashboard:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`
   - `MERCADOPAGO_PUBLIC_KEY`
   - `MERCADOPAGO_ACCESS_TOKEN`

4. **Deploy** (automatic on git push)

5. **Run migrations** via Railway CLI:
   ```bash
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   ```

### Render

1. **Create a new Web Service** on Render dashboard

2. **Connect your repository**

3. **Configure build and start commands**:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn config.wsgi:application`

4. **Set environment variables** in Render dashboard

5. **Deploy** (automatic)

### DigitalOcean App Platform

1. **Create a new app** on DigitalOcean

2. **Connect repository**

3. **Configure environment variables**

4. **Set build and run commands**:
   - Build: `pip install -r requirements.txt`
   - Run: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

5. **Deploy**

## Database Setup

### Using SQLite (Default)

SQLite is configured by default and works well for small to medium applications. No additional setup required.

### Using PostgreSQL (Optional)

1. **Add DATABASE_URL to environment variables**:
   ```bash
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

2. **Update settings.py** (already configured to use DATABASE_URL if provided)

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

## Pre-Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Generate and set a new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up MercadoPago credentials
- [ ] Run `python manage.py check --deploy` to verify configuration
- [ ] Test the application locally with production settings
- [ ] Ensure all migrations are applied
- [ ] Create a superuser account
- [ ] Collect static files

## Post-Deployment Steps

1. **Verify health check endpoint**:
   ```bash
   curl https://your-domain.com/health/
   ```

2. **Create superuser** (if not done during deployment):
   ```bash
   python manage.py createsuperuser
   ```

3. **Load initial data** (optional):
   ```bash
   python manage.py populate_db
   ```

4. **Test critical functionality**:
   - User registration and login
   - Product browsing
   - Cart operations
   - Checkout process
   - Payment integration
   - Admin panel access

## Monitoring and Maintenance

### Health Check

The application includes a health check endpoint at `/health/` that returns:
- Application status
- Database connectivity
- Debug mode status

### Logs

View application logs:

**Heroku**:
```bash
heroku logs --tail
```

**Railway**:
```bash
railway logs
```

**Render**: View logs in the dashboard

### Database Backups

**Heroku**:
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

**Railway/Render**: Use platform-specific backup features

## Troubleshooting

### Static Files Not Loading

1. Ensure `STATIC_ROOT` is configured
2. Run `python manage.py collectstatic`
3. Verify whitenoise is in `MIDDLEWARE`

### Database Connection Errors

1. Check `DATABASE_URL` environment variable
2. Verify database credentials
3. Ensure database is accessible from deployment platform

### 500 Internal Server Error

1. Check application logs
2. Verify all environment variables are set
3. Ensure `DEBUG=False` and `ALLOWED_HOSTS` is configured
4. Run `python manage.py check --deploy`

### CSRF Verification Failed

1. Ensure `CSRF_TRUSTED_ORIGINS` includes your domain
2. Verify HTTPS is enabled
3. Check cookie settings

## Security Recommendations

1. **Never commit `.env` file** to version control
2. **Use strong SECRET_KEY** in production
3. **Enable HTTPS** on your domain
4. **Regular security updates**: Keep Django and dependencies updated
5. **Monitor logs** for suspicious activity
6. **Set up database backups**
7. **Use environment variables** for all sensitive data

## Scaling Considerations

As your application grows:

1. **Upgrade to PostgreSQL** for better performance and features
2. **Add Redis** for caching and session storage
3. **Configure CDN** for static files and media
4. **Increase worker count** in Procfile
5. **Set up monitoring** (Sentry, New Relic, etc.)
6. **Implement rate limiting** for API endpoints

## Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Review deployment platform documentation
- Check application logs for error details
