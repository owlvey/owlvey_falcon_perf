
kubectl apply -f deploy-performance.yaml

kubectl apply -f route-performance.yaml

TIMEOUT 10

kubectl get pods -n owlvey -o wide