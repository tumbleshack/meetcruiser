npx openapi-generator-cli generate -g typescript-axios -i ../apispec.json -o ./tmp/api
npx tsc --project tsconfig.json