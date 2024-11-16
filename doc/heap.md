author: ouuan, HeRaNO

堆是一棵树，其每个节点都有一个键值，且每个节点的键值都大于等于/小于等于其父亲的键值。

每个节点的键值都大于等于其父亲键值的堆叫做小根堆，否则叫做大根堆。[STL 中的 `priority_queue`](container-adapter.md#优先队列) 其实就是一个大根堆。

（小根）堆主要支持的操作有：插入一个数、查询最小值、删除最小值、合并两个堆、减小一个元素的值。

一些功能强大的堆（可并堆）还能（高效地）支持 merge 等操作。

一些功能更强大的堆还支持可持久化，也就是对任意历史版本进行查询或者操作，产生新的版本。

## 堆的分类

|    操作 `\` 数据结构[^ref4]   |                                      配对堆                                     |      二叉堆     |      左偏树     |          二项堆         |        斐波那契堆       |
| :---------------------: | :--------------------------------------------------------------------------: | :----------: | :----------: | :------------------: | :----------------: |
|        插入（insert）       |                                    $O(1)$                                    |  $O(\log n)$ |  $O(\log n)$ |  $O(\log n)$[^ref1]  |       $O(1)$       |
|     查询最小值（find-min）     |                                    $O(1)$                                    |    $O(1)$    |    $O(1)$    | $O(1)$[^ref2][^ref3] |       $O(1)$       |
|    删除最小值（delete-min）    |                              $O(\log n)$[^ref3]                              |  $O(\log n)$ |  $O(\log n)$ |      $O(\log n)$     | $O(\log n)$[^ref3] |
|        合并 (merge)       |                                    $O(1)$                                    |    $O(n)$    |  $O(\log n)$ |      $O(\log n)$     |       $O(1)$       |
| 减小一个元素的值 (decrease-key) | $o(\log n)$（下界 $\Omega(\log \log n)$，上界 $O(2^{2\sqrt{\log \log n}})$）[^ref3] |  $O(\log n)$ |  $O(\log n)$ |      $O(\log n)$     |    $O(1)$[^ref3]   |
|         是否支持可持久化        |                                   $\times$                                   | $\checkmark$ | $\checkmark$ |     $\checkmark$     |      $\times$      |

[^ref1]: 单次插入的复杂度为 $O(\log n)$，但有 $k$ 次连续插入时，可创建一个只包含要插入元素的二项堆，再将此堆与原先的二项堆进行合并，均摊复杂度为 $O(1)$

[^ref2]: 可以保存一个指向最小元素的指针，在执行其他操作时修改该指针，即可在 $O(1)$ 的复杂度下进行查询了

[^ref3]: 复杂度为均摊复杂度

[^ref4]: 表格来自于 [Wikipedia](https://en.wikipedia.org/wiki/Priority_queue#Summary_of_running_times)

习惯上，不加限定提到「堆」时往往都指二叉堆。