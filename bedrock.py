import boto3

bedrock = boto3.client('bedrock')

def get_embeddings_bedrock(text):
  response = bedrock.invoke_model(
      modelId="amazon.titan.text-embedding",
      body={"input": text}
  )
  embedding_vector = response["embedding"]
  return embedding_vector