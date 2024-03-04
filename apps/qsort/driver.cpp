#include <cstdint>
#include <cstring>
#include <iostream>

#define TYPE uint8_t

using namespace std;

int partition(TYPE *arr, int left, int right) {
    TYPE pivot = arr[right];
    TYPE temp;
    int i = left - 1;
    for (int j = left; j < right; j++) {
        if (arr[j] <= pivot) {
            i += 1;
            temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    temp = arr[i + 1];
    arr[i + 1] = arr[right];
    arr[right] = temp;

    return i + 1;
}

/*
void qsort(TYPE *arr, int start, int end) {
    if (start < end) {
        int pivot = partition(arr, start, end);
        qsort(arr, start, pivot - 1);
        qsort(arr, pivot + 1, end);
    }
}
*/

void qsort(TYPE *arr, int start, int end) {
    if (end - start + 1 <= 1)
        return;
    int *stack = (int* )malloc(sizeof(int) * (end - start + 1));
    int top = -1;

    stack[++top] = start;
    stack[++top] = end;

    while (top >= 0) {
        end = stack[top--];
        start = stack[top--];

        int p = partition(arr, start, end);

        if (p - 1 > start) {
            stack[++top] = start;
            stack[++top] = p - 1;
        }
        if (p + 1 < end) {
            stack[++top] = p + 1;
            stack[++top] = end;
        }
    }
    free(stack);
}

extern "C"
int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size)
{
  TYPE *tmp = new TYPE[Size];
  memcpy(tmp, Data, Size);

  int n = Size / sizeof(TYPE);

  qsort(tmp, 0, n - 1);
  /*
  for (int i = 0; i < n; i++)
  {
    cout << (int)tmp[i] << endl;
  }
  */

  delete[] tmp;
  return 0;
}


