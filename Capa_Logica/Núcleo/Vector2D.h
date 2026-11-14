#pragma once
// Vector 2D en píxeles. Convención de pantalla: x crece a la derecha, y crece HACIA ABAJO.
#include <cmath>

struct Vector2D {
    double x = 0.0;
    double y = 0.0;

    constexpr Vector2D() = default;
    constexpr Vector2D(double x_, double y_) : x(x_), y(y_) {}

    constexpr Vector2D operator+(const Vector2D& o) const { return {x + o.x, y + o.y}; }
    constexpr Vector2D operator-(const Vector2D& o) const { return {x - o.x, y - o.y}; }
    constexpr Vector2D operator*(double k) const { return {x * k, y * k}; }
    constexpr Vector2D operator/(double k) const { return {x / k, y / k}; }
    constexpr Vector2D operator-() const { return {-x, -y}; }
    Vector2D& operator+=(const Vector2D& o) { x += o.x; y += o.y; return *this; }
    Vector2D& operator-=(const Vector2D& o) { x -= o.x; y -= o.y; return *this; }
    Vector2D& operator*=(double k) { x *= k; y *= k; return *this; }

    double magnitud() const { return std::hypot(x, y); }
    Vector2D normalizado() const {
        const double m = magnitud();
        return m > 1e-12 ? Vector2D(x / m, y / m) : Vector2D();
    }
    double distancia(const Vector2D& o) const { return (*this - o).magnitud(); }
    constexpr double punto(const Vector2D& o) const { return x * o.x + y * o.y; }
    double angulo() const { return std::atan2(y, x); }
    Vector2D rotado(double rad) const {
        const double c = std::cos(rad), s = std::sin(rad);
        return {x * c - y * s, x * s + y * c};
    }
    static Vector2D desdeAngulo(double rad, double magnitud = 1.0) {
        return {std::cos(rad) * magnitud, std::sin(rad) * magnitud};
    }
};

constexpr Vector2D operator*(double k, const Vector2D& v) { return v * k; }
