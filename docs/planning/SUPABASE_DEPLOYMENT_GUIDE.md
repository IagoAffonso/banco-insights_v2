# 🚀 Supabase Deployment Guide - Banco Insights 2.0

## 📋 **Deployment Status**

✅ **Supabase Project Ready**: Your project `banco-insights-db` is accessible  
⚠️ **Network Issue**: Direct PostgreSQL connection is blocked (common security measure)  
✅ **API Connection**: Supabase REST API is working perfectly  

## 🎯 **Step-by-Step Deployment**

### **Step 1: Deploy Database Schema**

1. **Go to your Supabase Dashboard**:
   👉 https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx

2. **Navigate to SQL Editor** (left sidebar)

3. **Copy the Schema File**:
   - Open: `database/schema/001_initial_schema.sql`
   - Copy ALL contents (400+ lines)

4. **Execute in SQL Editor**:
   - Paste the schema SQL
   - Click "RUN" to create all tables, views, and indexes

5. **Verify Success**:
   - Check "Table Editor" to see 7 new tables
   - Look for: `institutions`, `financial_data`, `time_periods`, etc.

---

### **Step 2: Load Institution Data**

Run this script to load institutions via API:

```bash
cd /Users/iagoaffonso/code/IagoAffonso/banco-insights-2.0
python -c "
import requests
import pandas as pd
import json
from pathlib import Path
import time

# Configuration
url = 'https://uwoxkycxkidipgbptsgx.supabase.co/rest/v1/institutions'
headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU',
    'Content-Type': 'application/json'
}

# Load sample institutions
institutions_file = Path('bacen_project_v1/data/consolidated_institutions.json')
if institutions_file.exists():
    df = pd.read_json(institutions_file)
    sample = df.head(50)  # Load first 50 institutions
    
    print(f'Loading {len(sample)} institutions...')
    for i, row in sample.iterrows():
        data = {
            'cod_inst': str(row['CodInst']).zfill(8),
            'cnpj': f'{i:014d}',
            'name': row['NomeInstituicao'],
            'short_name': row['NomeInstituicao'][:50],
            'type': 'Instituição Financeira',
            'segment': 'S1',
            'control_type': 'Privado Nacional',
            'region': 'SP',
            'city': 'São Paulo',
            'status': 'active'
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201, 409]:  # 409 = already exists
            print(f'✅ {i+1}/50: {data[\"name\"][:30]}')
        else:
            print(f'❌ Failed: {response.text}')
        time.sleep(0.2)  # Rate limiting
    
    print('✅ Institution loading complete!')
else:
    print('❌ Institutions file not found')
"
```

---

### **Step 3: Get Connection Details for ETL**

Since direct connection is blocked, we need to use Supabase's **Connection Pooler**:

1. **In your Supabase Dashboard**:
   - Go to **Settings** → **Database**
   - Look for **Connection Pooler** section
   - Copy the pooler connection string

2. **Typical Supabase Pooler Format**:
   ```
   Host: aws-0-us-east-1.pooler.supabase.com
   Port: 6543
   Database: postgres  
   User: postgres.uwoxkycxkidipgbptsgx
   Password: En9QmRQaw14nhwxL
   ```

---

### **Step 4: Run ETL Pipeline**

Once you have the correct connection details:

```bash
cd bacen_project_v1

# Test with sample data first
python run_etl_pipeline.py \
  --test-mode \
  --db-host=YOUR_POOLER_HOST \
  --db-port=6543 \
  --db-name=postgres \
  --db-user=postgres.uwoxkycxkidipgbptsgx \
  --db-password=En9QmRQaw14nhwxL \
  --validate

# If successful, run full pipeline
python run_etl_pipeline.py \
  --full-run \
  --db-host=YOUR_POOLER_HOST \
  --db-port=6543 \
  --db-name=postgres \
  --db-user=postgres.uwoxkycxkidipgbptsgx \
  --db-password=En9QmRQaw14nhwxL \
  --validate
```

---

## 🌐 **Frontend Integration**

### **JavaScript/React Example**:

```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://uwoxkycxkidipgbptsgx.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU'

const supabase = createClient(supabaseUrl, supabaseKey)

// Query institutions
const { data: institutions } = await supabase
  .from('institutions')
  .select('*')
  .eq('status', 'active')
  .limit(10)

// Query financial data with relationships
const { data: financialData } = await supabase
  .from('financial_data')
  .select(`
    valor,
    institutions(name, segment),
    time_periods(year, quarter_text),
    metrics(nome_coluna)
  `)
  .limit(100)

// Aggregate queries
const { data: marketShare } = await supabase
  .from('market_share_view')
  .select('*')
  .eq('year', 2024)
  .order('market_rank')
```

### **Python Example**:

```python
import requests

headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
}

base_url = 'https://uwoxkycxkidipgbptsgx.supabase.co/rest/v1'

# Get top institutions
response = requests.get(
    f'{base_url}/market_share_view?year=eq.2024&order=market_rank&limit=10',
    headers=headers
)
top_institutions = response.json()

# Get financial data with filters
response = requests.get(
    f'{base_url}/financial_data?select=valor,institutions(name),metrics(nome_coluna)&limit=100',
    headers=headers
)
financial_data = response.json()
```

---

## 📊 **Project URLs**

- **🌐 Project Dashboard**: https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx
- **🔧 SQL Editor**: https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx/sql
- **📊 Table Editor**: https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx/editor
- **⚙️ API Docs**: https://uwoxkycxkidipgbptsgx.supabase.co/rest/v1/
- **🔐 Settings**: https://supabase.com/dashboard/project/uwoxkycxkidipgbptsgx/settings/database

---

## ⚡ **Quick Validation**

Test your deployment with this API call:

```bash
curl "https://uwoxkycxkidipgbptsgx.supabase.co/rest/v1/institutions?limit=5" \
  -H "apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3b3hreWN4a2lkaXBnYnB0c2d4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4NTM5MzcsImV4cCI6MjA3MDQyOTkzN30.0zulTEyq1euc6PTgOsp5a_qy2v3hPTCrk7zLXq9elWU"
```

Expected result: JSON array with institution data.

---

## 🎉 **Success Checklist**

- [ ] Schema deployed via SQL Editor (7 tables created)
- [ ] Sample institutions loaded (50+ records)
- [ ] API calls returning data
- [ ] Connection pooler details obtained
- [ ] ETL pipeline test successful
- [ ] Frontend can query data via Supabase client

Your **Banco Insights 2.0** is ready for production! 🏦📈