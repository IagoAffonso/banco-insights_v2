# 🏛️ BACEN IFDATA API Documentation

**Source**: [BACEN IFDATA API v1](https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/documentacao)  
**Last Updated**: Based on official BACEN documentation  
**Purpose**: Brazilian Central Bank Selected Financial Institution Data API

---

## 📋 API Overview

- **Service Name**: IFData - Selected Financial Institution Data
- **Version**: v1
- **Protocol**: OData (Open Data Protocol)
- **Access Type**: Anonymous (no authentication required)
- **Base URL**: `https://olinda.bcb.gov.br/olinda/servico/IFDATA/versao/v1/odata`
- **Language Support**: Portuguese and English

## 🔗 Key Endpoints

### 1. IfDataCadastro - Financial Institution Registry

**Purpose**: Provides comprehensive information about financial institutions registered with BACEN.

**Parameters**:
- **AnoMes** (Required): Year-Month in AAAAMM format (e.g., 202403 for March 2024)

**Key Fields**:
- `CNPJ` - National Registry of Legal Entities
- `CodInst` - Institution Code
- `NomeInstituicao` - Institution Name
- `DataInicioAtividade` - Activity Start Date
- `TipoConsolidacao` - Consolidation Type
- `TipoControle` - Control Type
- `Segmento` - Segment Classification
- `Estado` - State
- `Municipio` - Municipality
- `Situacao` - Status (Active/Inactive)

### 2. ListaDeRelatorio - Report List

**Purpose**: Lists all available financial reports and their corresponding codes.

**Parameters**: None required

**Returns**:
- Report numbers
- Report names and descriptions
- Available periods

### 3. IfDataValores - Financial Reports Data

**Purpose**: Provides detailed financial report data with structure and column values.

**Required Parameters**:
- **AnoMes**: Year-Month (AAAAMM format)
- **TipoInstituicao**: Institution Type code
- **Relatorio**: Report Number

**Key Fields**:
- Report structure information
- Column definitions
- Financial values and metrics
- Institutional identifiers

## 📊 Data Types and Formats

### Supported Data Types
- **Decimal**: Financial amounts and ratios
- **Integer**: Counts and codes
- **Text**: Names, descriptions, and classifications
- **Date**: Formatted as AAAAMM or full dates

### Date Format
- **Standard Format**: AAAAMM (Year-Month)
- **Example**: 202403 = March 2024
- **Range**: Historical data available from 2013

## 🔍 Query Options (OData Parameters)

### Content and Format Control
- **$format**: Specify content type (json, xml, etc.)
- **$metadata**: Get service metadata

### Data Selection
- **$select**: Choose specific properties to return
  - Example: `$select=NomeInstituicao,CodInst`

### Filtering
- **$filter**: Apply filters to entities
  - Example: `$filter=TipoInstituicao eq 1`
  - Operators: eq (equal), ne (not equal), gt (greater than), lt (less than)

### Ordering and Pagination
- **$orderby**: Sort results
  - Example: `$orderby=NomeInstituicao asc`
- **$skip**: Skip number of results (pagination)
- **$top**: Limit maximum results returned

## 🏦 Institution Classification

### Institution Types (TipoInstituicao)
The API categorizes financial institutions into different types:
- **Type 1**: Commercial Banks
- **Type 2**: Multiple Service Banks and Other Institutions
- **Additional types**: Credit Cooperatives, Investment Banks, etc.

### Consolidation Types
- Individual institution data
- Consolidated group data
- Prudential consolidation

### Control Types
- **Public**: Government-controlled institutions
- **Private National**: Domestic private institutions
- **Private Foreign**: Foreign-controlled institutions

### Segments
- **S1**: Large institutions (≥ 10% market share)
- **S2**: Medium institutions (0.1% to 10% market share)
- **S3**: Small institutions (< 0.1% market share)
- **S4**: Credit cooperatives
- **S5**: Other institutions

## 📈 Available Financial Reports

The API provides access to multiple quarterly financial reports:

### Core Reports
1. **Resumo** (Summary) - Key financial metrics
2. **Ativo** (Assets) - Asset composition and details
3. **Passivo** (Liabilities) - Liability structure
4. **Patrimônio Líquido** (Shareholders' Equity)
5. **Demonstração de Resultado** (Income Statement)

### Credit Portfolio Reports
6. **Carteira de Crédito** - Credit portfolio details
7. **Crédito PF** - Individual person credit
8. **Crédito PJ** - Legal entity credit
9. **Provisões** - Credit loss provisions

### Specialized Reports
10. **Captações** - Funding and deposits
11. **Aplicações Interfinanceiras** - Interbank applications
12. **Títulos e Valores Mobiliários** - Securities portfolio
13. **Derivativos** - Derivative instruments
14. **Câmbio** - Foreign exchange operations

## 🔧 Technical Specifications

### API Limits
- Anonymous access (no rate limits specified)
- Large datasets available
- Historical data from 2013 onwards

### Response Formats
- **Primary**: JSON
- **Alternative**: XML, CSV (via $format parameter)
- **Encoding**: UTF-8

### Error Handling
- Standard HTTP status codes
- OData error format for invalid queries
- Descriptive error messages in Portuguese

## 💡 Usage Examples

### Get Institution Registry for March 2024
```
GET /IfDataCadastro?$filter=AnoMes eq 202403
```

### Get Credit Portfolio Report for Large Banks
```
GET /IfDataValores?AnoMes=202403&TipoInstituicao=1&Relatorio=6
```

### List All Available Reports
```
GET /ListaDeRelatorio
```

## 📊 Data Quality Notes

### Completeness
- Quarterly reporting cycle
- Some institutions may not report all metrics
- Historical consistency maintained

### Updates
- Data typically available 45-60 days after quarter end
- Revisions possible for recent periods
- Final data considered stable after 6 months

### Coverage
- All supervised financial institutions
- Individual and consolidated views available
- Geographic coverage: All Brazilian states

## 🎯 Integration Recommendations

### For Banco Insights 2.0
1. **Primary Endpoint**: Use `IfDataValores` for main data
2. **Institution Lookup**: Use `IfDataCadastro` for institution details
3. **Report Discovery**: Use `ListaDeRelatorio` for available reports
4. **Filtering**: Apply institution type and date filters
5. **Pagination**: Use $top and $skip for large datasets

### Best Practices
- Cache report lists (ListaDeRelatorio) as they change infrequently
- Implement retry logic for network timeouts
- Use $select to minimize payload size
- Monitor for data updates and revisions

---

**Note**: This documentation is based on the official BACEN IFDATA API documentation. For the most current information, always refer to the official source at the URL provided above.