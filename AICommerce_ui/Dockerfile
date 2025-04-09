# 1️⃣ Use Node.js image to build the React app
FROM node:18 AS build

# 2️⃣ Set the working directory inside the container
WORKDIR /app

# 3️⃣ Copy all files from local project folder to container
COPY . .

# 4️⃣ Install project dependencies (React + npm packages)
RUN npm install

# 5️⃣ Build the production version of the React app
RUN npm run build

# 6️⃣ Use Nginx to serve the built React app
FROM nginx:alpine

# 7️⃣ Copy the production-ready build from the previous stage to Nginx's default HTML folder
COPY --from=build /app/build /usr/share/nginx/html

# 8️⃣ (Optional) Replace Nginx default config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# 9️⃣ Expose port 80 for web traffic
EXPOSE 80

# 🔟 Start the Nginx server in foreground
CMD ["nginx", "-g", "daemon off;"]
