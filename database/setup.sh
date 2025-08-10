#!/bin/bash

# Banco Insights 2.0 - Database Setup Script
# Complete local development setup with testing

set -e  # Exit on any error

echo "🏦 Banco Insights 2.0 - Database Setup"
echo "====================================="

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_step "Checking Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_status "Docker is running ✅"
}

# Check Python dependencies
check_python() {
    print_step "Checking Python dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+."
        exit 1
    fi
    
    # Check if required packages are installed
    python3 -c "import asyncpg, pandas" 2>/dev/null || {
        print_warning "Installing required Python packages..."
        pip install asyncpg pandas
    }
    
    print_status "Python dependencies ready ✅"
}

# Start database services
start_services() {
    print_step "Starting database services..."
    
    # Stop any existing services
    docker-compose down --remove-orphans 2>/dev/null || true
    
    # Start services
    docker-compose up -d
    
    # Wait for PostgreSQL to be ready
    print_step "Waiting for PostgreSQL to be ready..."
    sleep 10
    
    # Check if PostgreSQL is ready
    max_attempts=30
    attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if docker-compose exec -T postgres pg_isready -U postgres -d banco_insights &>/dev/null; then
            print_status "PostgreSQL is ready ✅"
            break
        fi
        
        attempt=$((attempt + 1))
        echo -n "."
        sleep 2
    done
    
    if [ $attempt -eq $max_attempts ]; then
        print_error "PostgreSQL failed to start within expected time"
        docker-compose logs postgres
        exit 1
    fi
}

# Run database tests
run_tests() {
    print_step "Running database schema tests..."
    
    if python3 test_local_setup.py; then
        print_status "All database tests passed ✅"
    else
        print_error "Database tests failed ❌"
        print_warning "Check the test output above for details"
        return 1
    fi
}

# Create sample environment file
create_env_file() {
    print_step "Creating sample environment files..."
    
    if [ ! -f "../.env.example" ]; then
        cat > ../.env.example << EOF
# Banco Insights 2.0 - Environment Configuration

# Local Development Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/banco_insights

# Supabase Configuration (fill these when deploying)
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Application Configuration
NODE_ENV=development
NEXT_PUBLIC_APP_NAME="Banco Insights 2.0"
NEXT_PUBLIC_APP_VERSION="2.0.0"
EOF
        print_status "Created .env.example file ✅"
    else
        print_status ".env.example already exists ✅"
    fi
}

# Display connection information
show_connection_info() {
    print_step "Database Connection Information"
    echo ""
    echo "📊 PostgreSQL Database:"
    echo "   Host: localhost"
    echo "   Port: 5432"
    echo "   Database: banco_insights"
    echo "   Username: postgres"
    echo "   Password: postgres"
    echo ""
    echo "🔧 pgAdmin (Database Management):"
    echo "   URL: http://localhost:5050"
    echo "   Username: admin@bancoinights.com"
    echo "   Password: admin"
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Database is ready for development"
    echo "   2. Run tests: python3 test_local_setup.py"
    echo "   3. For Supabase deployment: cd supabase && python3 deploy.py"
    echo "   4. Connect your frontend to: postgresql://postgres:postgres@localhost:5432/banco_insights"
    echo ""
}

# Cleanup function
cleanup_on_error() {
    print_error "Setup failed. Cleaning up..."
    docker-compose down --remove-orphans 2>/dev/null || true
    exit 1
}

# Set trap for cleanup on error
trap cleanup_on_error ERR

# Main setup process
main() {
    echo ""
    print_step "Starting Banco Insights 2.0 database setup..."
    echo ""
    
    check_docker
    check_python
    start_services
    create_env_file
    
    # Run tests (allow to continue even if tests fail)
    set +e  # Don't exit on error for tests
    run_tests
    test_result=$?
    set -e  # Re-enable exit on error
    
    echo ""
    echo "🎉 Database setup completed!"
    echo "================================"
    
    if [ $test_result -eq 0 ]; then
        print_status "All tests passed - Database is fully ready! ✅"
    else
        print_warning "Setup complete but some tests failed - Check logs above ⚠️"
    fi
    
    show_connection_info
}

# Handle script arguments
case "${1:-}" in
    "test")
        print_step "Running tests only..."
        run_tests
        ;;
    "start")
        print_step "Starting services only..."
        check_docker
        start_services
        show_connection_info
        ;;
    "stop")
        print_step "Stopping services..."
        docker-compose down
        print_status "Services stopped ✅"
        ;;
    "restart")
        print_step "Restarting services..."
        docker-compose down
        start_services
        print_status "Services restarted ✅"
        ;;
    "clean")
        print_step "Cleaning up all resources..."
        docker-compose down --volumes --remove-orphans
        docker system prune -f
        print_status "Cleanup completed ✅"
        ;;
    "help"|"--help"|"-h")
        echo ""
        echo "Banco Insights 2.0 - Database Setup Script"
        echo "Usage: ./setup.sh [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)  - Full setup process"
        echo "  test       - Run database tests only"
        echo "  start      - Start services only"
        echo "  stop       - Stop all services"
        echo "  restart    - Restart all services"
        echo "  clean      - Clean up all resources"
        echo "  help       - Show this help"
        echo ""
        ;;
    *)
        main
        ;;
esac