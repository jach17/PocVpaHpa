// <summary>
// <copyright file="ITestsDao.cs" company="Axity">
// This source code is Copyright Axity and MAY NOT be copied, reproduced,
// published, distributed or transmitted to or stored in any manner without prior
// written consent from Axity (www.axity.com).
// </copyright>
// </summary>

namespace Toks.Loyalty.test.Persistence.DAO.Tests
{
    /// <summary>
    /// Interface ITestsDao.
    /// </summary>
    public interface ITestsDao
    {
        /// <summary>
        /// Method for Save Async.
        /// </summary>
        /// <returns>A <see cref="Task{TResult}"/> representing the result of the asynchronous operation.</returns>
        Task<int> SaveChangesAsync();
    }
}
