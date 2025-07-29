# On utilise une image de Caddy spéciale pour construire
FROM caddy:2-builder AS builder

# On construit Caddy en ajoutant le plugin de sécurité
RUN xcaddy build \
    --with github.com/greenpau/caddy-security

# On démarre avec une image Caddy propre et légère
FROM caddy:2-alpine

# On copie notre Caddy personnalisé depuis l'étape de construction
COPY --from=builder /usr/bin/caddy /usr/bin/caddy

# On copie notre Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile