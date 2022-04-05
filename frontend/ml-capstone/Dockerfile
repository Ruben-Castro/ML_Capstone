FROM node
WORKDIR '/app'
# This is an optimizatiion step seperate layer 
COPY package.json . 

#install our dev packages 
RUN npm install 

#copy over all of the source code
COPY . .

#Expose port 3000 
EXPOSE 3000


CMD ["npm", "start"]

