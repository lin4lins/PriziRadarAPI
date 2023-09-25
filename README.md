# Prizi Radar API

## Introduction

Prizi Radar API is a powerful tool designed to help users select a random comment from an Instagram (IG) post of a user. This API exclusively supports JSON as its content type.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [User Requirements](#user-requirements)
- [How It Works](#how-it-works)
  - [Registration](#registration)
  - [Linking IG Accounts](#linking-ig-accounts)
  - [Selecting Random Comments](#selecting-random-comments)

## Getting Started

Let's get started with Prizi Radar API.

### Prerequisites

Before using Prizi Radar API, make sure you have the following:

- Git installed on your system for cloning the repository.
- Docker Compose installed on your system.

### Installation

Clone the repository, navigate to the project directory, and start the Docker containers:

```bash
# Clone the repository
git clone https://github.com/lin4lins/PriziRadarAPI.git

# Change directory
cd PriziRadarAPI

# Start the Docker containers
docker compose up

```
## User Requirements
To use Prizi Radar API, users must meet the following requirements:

1. Have a Facebook (FB) account.
2. Have a connected Instagram (IG) account.
3. The connected IG account must be of the business type.

## How It Works
Prizi Radar API simplifies the process of selecting random comments from Instagram posts. Here's a detailed breakdown of how it works:

### Registration
To get started, users need to register with the API. Send a POST request to /users/ with the user's email and password. If the data is valid, the API will respond with a token.

```shell
curl -X POST -H "Content-Type: application/json" -d '{
  "email": "user@example.com",
  "password": "securepassword"
}' https://api.example.com/users/
```

### Linking IG Accounts
Users can link multiple IG accounts to the API. Send a POST request to /ig-accounts/ with the IG access token.

```shell
curl -X POST -H "Content-Type: application/json" -d '{
  "access_token": "your-ig-access-token"
}' https://api.example.com/ig-accounts/
```

### Selecting Random Comments
Once IG accounts are linked, users can select random comments from Instagram posts. Send a POST request to the API with the URL of the Instagram post and the account ID. The API will respond with data containing the comment author's username and text.

```shell
curl -X POST -H "Content-Type: application/json" -d '{
  "post_url": "https://www.instagram.com/p/your-post-id/",
  "account_id": "your-account-id"
}' https://api.example.com/select-comment/
```
