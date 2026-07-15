# Parse, Don't Validate Patterns

## Validator Smell

```typescript
validateEmail(input);
sendEmail(input);
```

The proof is lost. `sendEmail` still accepts any string.

## Parser Pattern

```typescript
const email = EmailAddress.parse(input);
sendEmail(email);
```

`sendEmail` now accepts only the parsed type.

## Boundary Rule

Parse at input boundaries and pass parsed values inward. Do not parse repeatedly in the core.
