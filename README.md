# sampled > smpld
## Secure Analysis of Multi-Party Large Encrypted Datasets
### Runtime Analysis
1. Start 3 servers which are able to communicate. E.g. inside the same AWS network.
2. Start the server script on each of these `screen python server.py`. You can detach the screen by pressing `CTRL+A` followed by `CTRL+D`. To resume later on, type  
`screen -r`.
3. Adjust the number of secrets you want to time inside *level0_create_encrypt_data.ipynb*.
4. Run the first 2 levels on each server, like `jupyter nbconvert --execute --to notebook --inplace level0_create_encrypt_data.ipynb && jupyter nbconvert --execute --to notebook --inplace level1_client_share_secrets.ipynb`.
5. Run the last level: `jupyter nbconvert --execute --to notebook --inplace level2_client_aggregate_secrets.ipynb`.
6. Check times inside *data/timer.csv*.
