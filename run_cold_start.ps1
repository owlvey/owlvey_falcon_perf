kubectl delete -f ./cluster/job-coldstart.yaml 

kubectl apply -f ./cluster/job-coldstart.yaml 

kubectl wait --for=condition=complete job/owlvey-api-coldstart-job -n owlvey --timeout=180s

$POD_NAME = kubectl get pods -l key=owlvey-api-coldstart-job -o=name -n owlvey

kubectl logs ${POD_NAME} -n owlvey
kubectl logs ${POD_NAME} -n owlvey > ./logs/integration_test.log

# kubectl cp -n owlvey ${POD_NAME}:/app ./logs/integration-test/ 






