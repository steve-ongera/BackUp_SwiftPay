# Swift Pay (POS) System

SwiftPay is a cutting-edge Point-of-Sale (POS) system designed to streamline transactions for businesses of all sizes. With an intuitive interface, real-time reporting, and secure payment processing, SwiftPay ensures seamless sales management. Features include inventory tracking, customer management, QR code generation, and integration with various payment platforms. SwiftPay is the ultimate solution for efficient, fast, and reliable point-of-sale operations.


![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Django](https://img.shields.io/badge/django-4.2%2B-green)

## 🚀 Features

### Sales Management
- **Quick Sale Processing**: Intuitive interface for rapid transaction handling
- **Real-time Stock Updates**: Automatic inventory adjustment after each sale
- **Multiple Payment Methods**: Support for cash, card, and mobile payments
- **Receipt Generation**: Automatic PDF receipt generation
- **Sale History**: Complete transaction history with detailed views
- **Returns/Refunds**: Process returns and refunds with inventory updates

### Inventory Management
- **Product Management**: Add, edit, and delete products
- **Stock Tracking**: Real-time inventory levels
- **Low Stock Alerts**: Automatic notifications for low stock items
- **Barcode Support**: Generate and scan product barcodes
- **Categories**: Organize products by categories
- **Bulk Import/Export**: CSV import/export for product data

### Customer Management
- **Customer Database**: Store and manage customer information
- **Purchase History**: Track customer purchase history
- **Loyalty Points**: Customer loyalty program support
- **Customer Categories**: Group customers by type
- **Credit Limits**: Set and manage customer credit limits

### Reporting
- **Sales Reports**: Daily, weekly, monthly, and custom period reports
- **Inventory Reports**: Stock levels, movement, and valuation
- **Financial Reports**: Revenue, profit margins, and tax reports
- **Customer Reports**: Customer purchase analysis
- **Export Options**: Export reports to PDF, Excel, or CSV

### Security
- **User Roles**: Admin, Manager, Cashier with different permissions
- **Audit Trail**: Track all system activities
- **Secure Authentication**: Role-based access control
- **Data Backup**: Automated backup systems

## 💻 Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL
- **CSS Framework**: Bootstrap 5
- **JavaScript Libraries**: 
  - jQuery for AJAX operations
  - DataTables for dynamic tables
  - Chart.js for reports visualization
- **PDF Generation**: xhtml2pdf
- **Barcode**: python-barcode
- **Testing**: pytest

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/steve-ongera/django-pos.git
cd django-pos
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Create .env file in project root
cp .env.example .env

# Update the following variables in .env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/pos_db
```

5. **Setup database**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_data.json
```

6. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` and log in with the superuser credentials.

## 📁 Project Structure

```
django-pos/
├── manage.py
├── requirements.txt
├── .env
├── pos/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── sales/
│   ├── products/
│   ├── customers/
│   ├── users/
│   └── reports/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── base.html
    └── components/
```

## 🚦 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run specific test file
pytest apps/sales/tests.py

# Run with coverage report
pytest --cov=apps
```

## 📝 Usage Guidelines

### Setting Up Products
1. Log in as admin
2. Go to Products > Add Product
3. Fill in required details:
   - Product name
   - SKU
   - Price
   - Category
   - Initial stock
4. Save the product

### Processing Sales
1. Click "New Sale" on the dashboard
2. Add products by:
   - Scanning barcode
   - Searching product name
   - Browsing categories
3. Adjust quantities if needed
4. Add customer details (optional)
5. Select payment method
6. Complete sale and print receipt

### Generating Reports
1. Go to Reports section
2. Select report type
3. Choose date range
4. Generate report
5. Export in desired format

## 🔐 Security Considerations

- Regular password updates recommended
- Session timeout after 30 minutes
- IP-based login restrictions available
- Failed login attempt monitoring
- Regular security audit logging

## 🔄 Backup and Recovery

### Automated Backups
- Daily database backups at 12 AM
- Stored in secure cloud storage
- Retention period: 30 days

### Manual Backup
```bash
python manage.py dbbackup
```

### Restore from Backup
```bash
python manage.py dbrestore
```

## 🛠 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check PostgreSQL service status
   - Verify database credentials in .env
   - Ensure database exists

2. **PDF Generation Errors**
   - Check wkhtmltopdf installation
   - Verify template syntax
   - Check file permissions

3. **Performance Issues**
   - Enable database query logging
   - Check index usage
   - Monitor server resources

## 📈 Roadmap

### Upcoming Features
- [ ] Mobile app integration
- [ ] Multi-store support
- [ ] Advanced analytics dashboard
- [ ] Supplier management
- [ ] Automated purchase orders

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 👥 Support

For support and queries:
- Create an issue
- Email: support@innovationhubsoftwaresltd.com
- Documentation: [docs.djangopos.com](https://docs.djangopos.com)

## 🙏 Acknowledgments

- Django community
- Bootstrap team
- All contributors

---
Made with ❤️ by steve ongera | 0112284093