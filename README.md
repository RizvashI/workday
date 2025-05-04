# workday
mixed arc
                             ┌────────────────────┐
                             │     Internet       │
                             └────────▲───────────┘
                                      │
                             ┌────────┴────────┐
                             │  Application LB │◄──── Optional
                             └────────▲────────┘
                                      │
                             ┌────────┴────────┐
                             │  Public Subnet  │
                             └────────▲────────┘
                                      │
                          ┌───────────┴────────────┐
                          │  Auto Scaling Group    │
                          │  (EC2 w/ Docker App)   │
                          └───────────▲────────────┘
                                      │
                     ┌────────────────┴──────────────┐
                     │     EC2 with bulls_web        │
                     │ - Port 8080                   │
                     │ - Docker + User Data          │
                     └─────────────┬─────────────────┘
                                   │
                        ┌──────────┴─────────────┐
                        │     Private Subnet     │
                        │ (No direct Internet)   │
                        └────────┬────┬──────────┘
                                 │    │
                ┌────────────────┘    └────────────────┐
                │                                     │
         ┌──────▼──────┐                     ┌────────▼────────┐
         │   AWS S3    │                     │   RDS / MySQL   │
         │ - Static    │                     │ - Persistent DB │
         │ - Backups   │                     │ - Leaderboard   │
         └─────────────┘                     └─────────────────┘

                        ┌────────────────────────────┐
                        │  Lambda functions (optional)│
                        │ - API / stats / auth       │
                        │ - Serverless extensions    │
                        └────────────────────────────┘
