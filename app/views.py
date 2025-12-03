from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .retriever import SimpleTFIDFRetriever


class RetrieverAPIView(APIView):
    def post(self, request):
        question = request.data.get("question", "").strip()
        top_k = int(request.data.get("top_k", 3))

        if not question:
            return Response(
                {"error": "Please enter a question."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cache_key = f"retreiver:{hash(question)}:{top_k}"
        cached_results = cache.get(cache_key)

        if cached_results:
            return Response(cached_results, status=status.HTTP_200_OK)

        retriever = SimpleTFIDFRetriever()
        results = retriever.query(question, top_k=top_k)

        data = {
            "results" : [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "score": round(score, 4),
                    "content": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                }
                for doc, score in results
            ],
            "total": len(results)
        }
        cache.set(cache_key, data, 300)
        return Response(data, status=status.HTTP_200_OK)