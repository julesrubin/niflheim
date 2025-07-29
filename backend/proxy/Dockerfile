# Use the xcaddy builder image as the first stage
FROM caddy:2-builder AS builder

# Use xcaddy to build a new Caddy binary that includes the google-id-token plugin
RUN xcaddy build \
    --with github.com/saviola/caddy-google-id-token

# Start a new, final stage from the standard caddy image
FROM caddy:2-alpine

# Copy the custom-built Caddy binary from the builder stage into the final image
COPY --from=builder /usr/bin/caddy /usr/bin/caddy

# Now, copy your Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile