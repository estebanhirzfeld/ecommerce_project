# 🚀 Quick Start: Deploy to Render

Follow these steps to deploy your e-commerce project to Render in minutes!

## ✅ Pre-Deployment Checklist

- [ ] Code is committed to Git
- [ ] Repository is pushed to GitHub
- [ ] You have a Render account (sign up at https://render.com)
- [ ] You have your MercadoPago API credentials ready

## 📋 Deployment Steps

### 1. Generate Secret Key

Run this command and save the output:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Push to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 3. Deploy on Render

**Option A: Blueprint (Easiest)**
1. Go to https://dashboard.render.com
2. Click **New +** → **Blueprint**
3. Connect your GitHub repository
4. Render will detect `render.yaml`
5. Set environment variables when prompted:
   - `ALLOWED_HOSTS`: (will be your-app.onrender.com)
   - `MERCADOPAGO_PUBLIC_KEY`: Your key
   - `MERCADOPAGO_ACCESS_TOKEN`: Your token
6. Click **Apply**

**Option B: Manual**
1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Connect your repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application`
5. Add environment variables (see below)
6. Click **Create Web Service**

### 4. Set Environment Variables

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | The key you generated in step 1 |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | Your Render URL (e.g., `your-app.onrender.com`) |
| `MERCADOPAGO_PUBLIC_KEY` | Your MercadoPago public key |
| `MERCADOPAGO_ACCESS_TOKEN` | Your MercadoPago access token |

### 5. Wait for Deployment

- Render will build your app (5-10 minutes)
- Watch the logs for any errors
- Once complete, you'll get a URL like `https://your-app.onrender.com`

### 6. Update ALLOWED_HOSTS

After deployment:
1. Copy your Render URL
2. Go to **Environment** tab
3. Update `ALLOWED_HOSTS` with your actual URL
4. Save (this triggers a redeploy)

### 7. Create Superuser

1. Go to your service → **Shell** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts to create admin account

### 8. Test Your Site

Visit these URLs:
- ✅ Homepage: `https://your-app.onrender.com/`
- ✅ Health: `https://your-app.onrender.com/health/`
- ✅ Admin: `https://your-app.onrender.com/admin/`
- ✅ Custom Admin: `https://your-app.onrender.com/custom-admin/`

## 🎉 You're Live!

Your e-commerce site is now deployed on Render!

## 📚 Need More Help?

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions and troubleshooting.

## ⚠️ Important Notes

- **Free tier**: App sleeps after 15 min of inactivity (30-60s cold start)
- **Automatic HTTPS**: SSL certificates included
- **Auto-deploy**: Pushes to main branch trigger redeployment
- **Logs**: Available in Render dashboard

## 🔄 Updating Your App

```bash
git add .
git commit -m "Update app"
git push origin main
```

Render automatically redeploys!
