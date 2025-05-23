from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal
from rest_framework.test import APIClient
from rest_framework import status


class AdTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Книга по Python',
            description='Отличная книга для изучения Python',
            category='books',
            condition='new'
        )
        
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Наушники',
            description='Беспроводные наушники',
            category='electronics',
            condition='used'
        )
        
        self.client = APIClient()
    
    def test_create_ad(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/ads/', {
            'title': 'Новое объявление',
            'description': 'Описание',
            'category': 'books',
            'condition': 'new'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 3)
    
    def test_edit_ad(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(f'/api/ads/{self.ad1.id}/', {
            'title': 'Обновленное название'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Обновленное название')
    
    def test_delete_ad(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/ads/{self.ad1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 1)
    
    def test_search_ads(self):
        response = self.client.get('/api/ads/?search=Python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Книга по Python')


class ExchangeProposalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Книга по Python',
            description='Отличная книга для изучения Python',
            category='books',
            condition='new'
        )
        
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Наушники',
            description='Беспроводные наушники',
            category='electronics',
            condition='used'
        )
        
        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Предлагаю обмен'
        )
        
        self.client = APIClient()
    
    def test_create_proposal(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/proposals/', {
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': 'Новое предложение'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExchangeProposal.objects.count(), 2)
    
    def test_accept_proposal(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/proposals/{self.proposal.id}/accept/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'accepted')
    
    def test_reject_proposal(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/proposals/{self.proposal.id}/reject/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'rejected')