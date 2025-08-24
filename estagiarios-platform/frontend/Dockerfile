FROM node:18-alpine

WORKDIR /app

# Copia package.json e package-lock.json
COPY package*.json ./

# Instala dependências
RUN npm ci --only=production

# Copia o código da aplicação
COPY . .

# Expõe a porta
EXPOSE 3000

# Comando para executar a aplicação
CMD ["npm", "start"]

