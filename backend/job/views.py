from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Min, Max, Count
from .filters import JobsFilter
from .serializers import JobSerializer, CandidatesAppliedSerializer, CandidatesFavoriteSerializer
from .models import Job, CandidatesApplied,CandidatesFavorite
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Create your views here.

@api_view(['GET'])

def getAllJobs(request):

    #jobs = Job.objects.all()
    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by('id'))
    count = filterset.qs.count()

    # Pagination
    resPerPage = filterset.qs.count()
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)
    
    serializer = JobSerializer(queryset, many=True)
    return Response({
        "count": count,
        "resPerPage": resPerPage,
        'jobs': serializer.data
        })

@api_view(['GET'])
def getJob(request, pk):
    job = get_object_or_404(Job, id=pk)

    cabdidatesApplied = job.candidatesapplied_set.all().count()
    
    serializer = JobSerializer(job, many=False)

    jobs = Job.objects.all().filter(education=serializer.data.education).count(6).order_by('id')

    return Response({'job':serializer.data, 'cabdidatesApplied':cabdidatesApplied, 'relatedJobs':jobs})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def newJob(request):
    print(request.data)
    request.data['remote'] = False
    request.data['user'] = request.user
    data = request.data

    job = Job.objects.create(**data)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateJob(request, pk):
    job = get_object_or_404(Job, id=pk)

    if job.user != request.user:
        return Response({ 'message': 'You can not update this job' }, status=status.HTTP_403_FORBIDDEN)

    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.jobType = request.data['jobType']
    job.education = request.data['education']
    job.industry = request.data['industry']
    job.experience = request.data['experience']
    job.salary = request.data['salary']
    job.positions = request.data['positions']
    job.company = request.data['company']
    job.remote = request.data['remote']

    job.save()

    serializer = JobSerializer(job, many=False)

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteJob(request, pk):
    job = get_object_or_404(Job, id=pk)

    if job.user != request.user:
        return Response({ 'message': 'You can not delete this job' }, status=status.HTTP_403_FORBIDDEN)

    job.delete()

    return Response({ 'message': 'Job is Deleted.' }, status=status.HTTP_200_OK)

@api_view(['GET'])
def getTopicStats(request, topic):

    if topic == 'java' or topic == 'Java':
        topic = 'java '
    
    args = { 'title__icontains': topic } # to check that title contains the topic word
    jobs = Job.objects.filter(**args)

    if len(jobs) == 0:
        return Response({ 'message': 'Not stats found for {topic}'.format(topic=topic) })

    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        avg_positions = Avg('positions'),
        avg_salary = Avg('salary'),
        min_salary = Min('salary'),
        max_salary = Max('salary')
    )

    return Response(stats)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applyToJob(request, pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)


    if job.lastDate < timezone.now():
        return Response({ 'error': 'You can not apply to this job. Date is over' }, status=status.HTTP_400_BAD_REQUEST)

    alreadyApplied = job.candidatesapplied_set.filter(user=user).exists()

    if alreadyApplied:
        return Response({ 'error': 'You have already apply to this job.' }, status=status.HTTP_400_BAD_REQUEST)


    jobApplied = CandidatesApplied.objects.create(
        job = job,
        user = user
    )

    return Response({
        'applied': True,
        'job_id': jobApplied.id
    },
    status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favoriteJob(request, pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    
    if job.lastDate < timezone.now():
        return Response({ 'error': 'You can not favorite this job as this ad is not valid!' }, status=status.HTTP_400_BAD_REQUEST)

    alreadyfavorite = job.candidatesfavorite_set.filter(user=user, favorite=True).exists()

    
    if alreadyfavorite:
        
        CandidatesFavorite.objects.filter(user=user, job=job).delete()
        return Response({
            'favorite': False,
            'message': 'Job is removed from your favorite list.'
        },
        status=status.HTTP_200_OK
        )
    else:
         jobFavorite = CandidatesFavorite.objects.create(
             job = job,
             user = user,
             favorite = True
         )
         return Response({
            'favorite': True,
            'message': 'Job is added to your favorite list.'
        },
        status=status.HTTP_200_OK
        )
    
   

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserAppliedJobs(request):

    args = { 'user_id': request.user.id }

    jobs = CandidatesApplied.objects.filter(**args)

    serializer = CandidatesAppliedSerializer(jobs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserFavoriteJobs(request):

    args = { 'user_id': request.user.id }


    jobs = CandidatesFavorite.objects.filter(**args)
    
    serializer = CandidatesFavoriteSerializer(jobs, many=True)
   
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def isApplied(request, pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    applied = job.candidatesapplied_set.filter(user=user).exists()

    return Response(applied)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserJobs(request):

    args = { 'user': request.user.id }

    jobs = Job.objects.filter(**args)
    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCandidatesApplied(request, pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    if job.user != user:
        return Response({ 'error': 'You can not acces this job' }, status=status.HTTP_403_FORBIDDEN)

    candidates = job.candidatesapplied_set.all()

    serializer = CandidatesAppliedSerializer(candidates, many=True)

    return Response(serializer.data)


@api_view(['GET'])

def getRemoteJobs(request):

    filterset = Job.objects.all().filter(remote=True).order_by('id')
    
    serializer = JobSerializer(filterset, many=True)
    return Response({
        'jobs': serializer.data[0:5]
        })

@api_view(['GET'])

def getHottestJobs(request):

    filterset = Job.objects.all().order_by('salary').reverse()
    
    serializer = JobSerializer(filterset, many=True)
    return Response({
        'jobs': serializer.data[0:8]
        })

@api_view(['GET'])

def getFresherJobs(request):

    filterset = Job.objects.all().filter(experience='No Experience').order_by('id')
    
    serializer = JobSerializer(filterset, many=True)
    return Response({
        'jobs': serializer.data[0:8]
        })

@api_view(['GET'])

def getNewestJobs(request):

    filterset = Job.objects.all().order_by('createdAt').reverse()
    
    serializer = JobSerializer(filterset, many=True)
    return Response({
        'jobs': serializer.data[0:5]
        })