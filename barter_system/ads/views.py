from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer
from django.contrib.auth.models import User


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'condition']
    search_fields = ['title', 'description']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'error': 'Вы не можете редактировать это объявление'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'error': 'Вы не можете удалить это объявление'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().order_by('-created_at')
    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Фильтрация по отправителю или получателю
        sent = self.request.query_params.get('sent', None)
        received = self.request.query_params.get('received', None)
        status = self.request.query_params.get('status', None)
        
        if sent == 'true':
            queryset = queryset.filter(ad_sender__user=user)
        if received == 'true':
            queryset = queryset.filter(ad_receiver__user=user)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            return Response(
                {'error': 'Вы не можете принять это предложение'},
                status=status.HTTP_403_FORBIDDEN
            )
        proposal.status = 'accepted'
        proposal.save()
        return Response({'status': 'предложение принято'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            return Response(
                {'error': 'Вы не можете отклонить это предложение'},
                status=status.HTTP_403_FORBIDDEN
            )
        proposal.status = 'rejected'
        proposal.save()
        return Response({'status': 'предложение отклонено'})
