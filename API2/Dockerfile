FROM openjdk:17-jdk-slim

# Establecer el directorio de trabajo
WORKDIR /app
# Copiar el archivo JAR de la aplicación al contenedor
COPY target/*.jar app.jar
# Exponer el puerto en el que la aplicación escuchará
EXPOSE 8080
# Comando para ejecutar la aplicación
CMD ["java", "-jar", "app.jar"]