
kubectl apply -f deploy-performance.yaml

kubectl apply -f route-performance.yaml

Start-Sleep 10

kubectl get pods -n owlvey -o wide