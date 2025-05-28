# Etapa de construcción
FROM openjdk:17-jdk-slim AS build

WORKDIR /app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
# COPY lib lib         # <-- COMENTA O ELIMINA ESTA LÍNEA
COPY src src

RUN chmod +x mvnw
RUN ./mvnw package -DskipTests

# Etapa final
FROM openjdk:17-slim

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-Dfile.encoding=UTF-8", "-jar", "app.jar"]