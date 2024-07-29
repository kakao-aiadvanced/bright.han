# Prompt Generation
## 안 되서 밑에꺼 씀
### https://chatgpt.com/g/g-nPwpAqi10-god-of-prompt/c/23d04ace-7fe3-4cde-a544-851862e48f91

### 질문

```
온콜문의가 runway api 문제인지 event-horizon 문제인지 nal-builder 문제인지 분류하고 어떤 한문장으로 정리해줘

I need to triage support requests that come in via on-call. Please categorize whether the issue is related to the Runway API, Event-Horizon, or Nal-Builder, and summarize in one sentence. 
```

### 답변
OPTION A
```
<Task>
Categorize on-call support requests as related to Runway API, Event-Horizon, or Nal-Builder, and provide a one-sentence summary.
</Task>
<Inputs>
{$SUPPORT_REQUEST}
</Inputs>
<Instructions>
You will categorize incoming support requests received via on-call and provide a one-sentence summary of the issue. Follow these steps:
1. Read the support request carefully.
2. Identify whether the issue is related to Runway API, Event-Horizon, or Nal-Builder.
3. Provide a one-sentence summary of the issue.
4. Write your categorization and summary inside <response> tags.

<response>
Category: [Runway API/Event-Horizon/Nal-Builder]
Summary: [One-Sentence Summary of the Issue]
</response>
</Instructions>
```

OPTION B
```
<Task>
Review on-call support requests to determine if the issue is related to Runway API, Event-Horizon, or Nal-Builder, and provide a brief summary.
</Task>
<Inputs>
{$ON_CALL_MESSAGE}
</Inputs>
<Instructions>
Your task is to review on-call support requests to categorize the issue and provide a brief summary. Here are the steps:
1. Analyze the content of the on-call support request.
2. Determine if the issue pertains to Runway API, Event-Horizon, or Nal-Builder.
3. Write a brief summary of the issue in one sentence.
4. Return your findings inside <triage> tags.

<triage>
Category: [Runway API/Event-Horizon/Nal-Builder]
Summary: [Brief Summary of the Issue]
</triage>
</Instructions>
```