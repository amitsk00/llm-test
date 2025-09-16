data = {
   "id":"0b83200e-ac06-46b2-a0d3-5e1a171b0dbd",
   "model":"sonar",
   "created":1757154908,
   "usage":{
      "prompt_tokens":30,
      "completion_tokens":357,
      "total_tokens":387,
      "search_context_size":"low",
      "cost":{
         "input_tokens_cost":0.0,
         "output_tokens_cost":0.0,
         "request_cost":0.005,
         "total_cost":0.005
      }
   },
   "citations":[
      "https://www.digitalocean.com/community/tutorials/create-a-partition-in-linux",
      "https://learn.microsoft.com/en-us/sql/relational-databases/partitions/partitioned-tables-and-indexes?view=sql-server-ver17",
      "https://www.hp.com/us-en/shop/tech-takes/how-to-partition-a-hard-drive",
      "https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-partition",
      "https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/5/html/installation_guide/ch-partitions-x86"
   ],
   "search_results":[
      {
         "title":"Create a Partition in Linux - A Step-by-Step Guide | DigitalOcean",
         "url":"https://www.digitalocean.com/community/tutorials/create-a-partition-in-linux",
         "date":"2022-08-03",
         "last_updated":"2025-09-06",
         "snippet":"In this tutorial, we'll be covering the steps to create a partition in Linux. This can help you allocate different memory regions for specific uses."
      },
      {
         "title":"Partitioned Tables and Indexes - SQL Server, Azure SQL Database ...",
         "url":"https://learn.microsoft.com/en-us/sql/relational-databases/partitions/partitioned-tables-and-indexes?view=sql-server-ver17",
         "date":"2025-07-29",
         "last_updated":"2025-09-05",
         "snippet":"A partition function is a database object that defines how the rows of a table or index are mapped to a set of partitions based on the values of a certain ..."
      },
      {
         "title":"How to Partition a Hard Drive in Windows 10/11 | HP® Tech Takes",
         "url":"https://www.hp.com/us-en/shop/tech-takes/how-to-partition-a-hard-drive",
         "date":"2024-08-08",
         "last_updated":"2025-09-05",
         "snippet":"In this guide, we'll walk you through the process of partitioning a hard drive using the built-in Windows Disk Management tool, available in both Windows 10 ..."
      },
      {
         "title":"Partitions | Databricks on AWS",
         "url":"https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-partition",
         "date":"2024-11-21",
         "last_updated":"2025-08-22",
         "snippet":"You use the PARTITION clause to identify a partition to be queried or manipulated. A partition is identified by naming all its columns and ..."
      },
      {
         "title":"Chapter 26. An Introduction to Disk Partitions | Installation Guide",
         "url":"https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/5/html/installation_guide/ch-partitions-x86",
         "date":"2023-01-11",
         "last_updated":"2025-09-06",
         "snippet":"This appendix uses a simplified diagram of a disk drive to help explain what is really happening when a disk drive is partitioned."
      }
   ],
   "object":"chat.completion",
   "choices":[
      {
         "index":0,
         "finish_reason":"stop",
         "message":{
            "role":"assistant",
            "content":"How to use partitions depends on the context—whether you mean disk partitions or data partitions in databases:\n\n**Disk Partitions (Linux, Windows, etc.):**\n\n- Partitions divide a physical hard drive into multiple logical sections. Each partition can hold a separate file system or operating system.  \n- To create or manage partitions in Linux, use tools like `fdisk` or `parted`. For example, using `fdisk` involves listing current partitions (`sudo fdisk -l`), selecting a disk (`sudo fdisk /dev/sdX`), and then creating or resizing partitions interactively[1][5].  \n- In Windows, use the Disk Management tool to create, delete, or format partitions, which appear as separate drives (C:, D:, etc.) for organizing data or installing multiple OSes[3].  \n- Partitions help with organizing files, dual-booting, improving performance, and protecting data in case of corruption.\n\n**Database Partitions (like SQL Server, Databricks):**\n\n- Database partitions split a table or index into parts based on column values (partition keys), improving query performance and manageability.  \n- For example, in SQL Server, you define a partition function that maps rows to partitions based on a column value range, often using date ranges for time-based data[2].  \n- Databricks SQL uses the PARTITION clause to specify partitions for querying or data manipulation[4].\n\nIn summary, **use disk partitions** to organize physical storage and install multiple OS or separate data, and **use database partitions** to optimize query performance by splitting tables based on column values. The specific tools and commands depend on your environment but typically involve selection of disks or columns, defining partition boundaries, and executing partitioning commands."
         },
         "delta":{
            "role":"assistant",
            "content":""
         }
      }
   ]
}

print(type(data))
print(data["usage"]["total_tokens"])


