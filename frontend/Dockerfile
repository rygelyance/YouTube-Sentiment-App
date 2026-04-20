FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Use Nginx to serve the static files professionally
FROM nginx:alpine
# Add a custom nginx config if necessary
COPY --from=build /app/dist /usr/share/nginx/html
# Ensure permissions are correct
RUN chmod -R 755 /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]