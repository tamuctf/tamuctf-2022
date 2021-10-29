FROM debian:buster-slim

# Update Items
RUN apt-get update -y
RUN apt-get install socat python3 python3-pip build-essential -y

# Add Items
ADD create.py /chal/create.py
ADD run.sh /chal/run.sh
WORKDIR /chal

# Expose the Port
EXPOSE 39193

# Make entrypoint executable
RUN chmod +x /chal/run.sh

# Entrypoint
ENTRYPOINT ["/chal/run.sh"]
