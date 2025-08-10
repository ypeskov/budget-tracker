# API Usage Examples for Deleting Templates

## Deleting Templates via DELETE /transactions/templates

### Option 1: Passing IDs through Query Parameter

```bash
# Delete one template
DELETE /transactions/templates?ids=1

# Delete multiple templates
DELETE /transactions/templates?ids=1,2,3

# Delete templates with spaces (automatically cleaned)
DELETE /transactions/templates?ids=1, 2, 3
```

### Request Examples

#### cURL
```bash
curl -X DELETE "http://localhost:8000/transactions/templates?ids=1,2,3" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### JavaScript/Fetch
```javascript
const response = await fetch('/transactions/templates?ids=1,2,3', {
  method: 'DELETE',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
});

const updatedTemplates = await response.json();
```

#### Python/requests
```python
import requests

response = requests.delete(
    'http://localhost:8000/transactions/templates',
    params={'ids': '1,2,3'},
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

updated_templates = response.json()
```

### Input Data Validation

The API automatically validates input data through the Pydantic schema `TemplateIdsSchema`:

- ✅ `ids=1,2,3` - correct
- ✅ `ids=1, 2, 3` - correct (spaces are automatically removed)
- ❌ `ids=` - error: "IDs cannot be empty"
- ❌ `ids=1,abc,3` - error: "Invalid ID format"
- ❌ `ids=1,0,3` - error: "All IDs must be positive integers"
- ❌ `ids=1,-2,3` - error: "All IDs must be positive integers"

### API Response

On successful deletion, an updated list of templates is returned:

```json
[
  {
    "id": 4,
    "categoryId": 2,
    "label": "Products",
    "category": {
      "id": 2,
      "name": "Products",
      "icon": "🍎"
    }
  }
]
```

### Error Handling

#### 400 Bad Request
```json
{
  "detail": "Invalid ID format: No valid IDs found"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Unable to delete templates"
}
```

## Additional Endpoint for Validation

### GET /transactions/templates/validate

Allows checking the correctness of ID format without performing deletion:

```bash
GET /transactions/templates/validate?ids=1,2,3
```

Response:
```json
[1, 2, 3]
```

## Advantages of the Current Approach

1. **Ease of use**: IDs are passed as a string through query parameter
2. **Pydantic validation**: Automatic data correctness checking
3. **Flexibility**: Support for various formats (with spaces, without spaces)
4. **Security**: Protection against SQL injection through validation
5. **Backward compatibility**: Easy to integrate with existing frontend

## Alternative Approaches

### Option 2: Passing through request body (not recommended for DELETE)
```json
{
  "ids": [1, 2, 3]
}
```

### Option 3: Passing through path parameters
```
DELETE /transactions/templates/1,2,3
```

The current approach with query parameters is the most standard and convenient for DELETE requests.
