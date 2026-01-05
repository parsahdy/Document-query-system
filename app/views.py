from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .models import Query
from .retriever import SimpleTFIDFRetriever
from .llmchain import answer_with_document


class RetrieverAPIView(APIView):
    def post(self, request):
        question = request.data.get("question", "").strip()
        top_k = int(request.data.get("top_k", 3))

        if not question:
            return Response(
                {"error": "Please enter a question."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cache_key = f"retriever:{hash(question)}:{top_k}"
        cached_results = cache.get(cache_key)

        if cached_results:
            query_obj, created = Query.objects.get_or_create(
                question=question,
                defaults={"processing_status": "Completed"}
            )
            if created or not query_obj.answer:
                query_obj.answer = cached_results["answer"]
                query_obj.related_docs.set(cached_results["doc_ids"])
                query_obj.mark_as_completed()
                query_obj.save()
            
            cached_results["query_id"] = query_obj.id
            return Response(cached_results, status=status.HTTP_200_OK)
        
        query_obj, created = Query.objects.get_or_create(
            question=question,
            defaults={"processing_status": "Processing"}
        )
        
        answer, results = answer_with_document(question, top_k)

        doc_ids = [doc.id for doc, score in results]

        query_obj.answer = answer
        query_obj.related_docs.set(doc_ids)
        query_obj.mark_as_completed()
        query_obj.save()

        data = {
            "query_id": query_obj.id,
            "answer": answer,
            "results": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "score": round(score, 4),
                    "content_preview": doc.content + "..." if len(doc.content) > 200 else doc.content
                }
                for doc, score in results
            ],
            "doc_ids": doc_ids,
            "total": len(results)
        }

        cache.set(cache_key, data, 300)
        return Response(data, status=status.HTTP_200_OK)