# Contributing to iVendNext AI Chat

Thank you for your interest in contributing to iVendNext AI Chat!

## Development Setup

1. Fork the repository
2. Clone your fork
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

## Development Workflow

### Backend Development

1. Make changes to Python files in `ivendnext_ai_chat/`
2. Test your changes
3. Run linting:
   ```bash
   black .
   flake8
   ```

### Frontend Development

1. Make changes to TypeScript/React files in `frontend/src/`
2. Run dev server:
   ```bash
   npm run dev
   ```
3. Build for production:
   ```bash
   npm run build
   ```

## Code Style

- Python: Follow PEP 8, use Black formatter
- TypeScript/React: Use ESLint and Prettier
- Commits: Use conventional commits format

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Update documentation
5. Submit PR with clear description

## Testing

```bash
# Python tests
pytest

# Frontend tests
npm test
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
